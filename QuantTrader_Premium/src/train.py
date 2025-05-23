# Python file
import os
import ray
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
from ray.tune.registry import register_env
import pandas as pd
from dotenv import load_dotenv
from src.env.stock_trading_env import StockTradingEnv

load_dotenv()


def load_data():
    data_path = os.path.join("data", "historical", "AAPL.csv")
    df = pd.read_csv(data_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def env_creator(env_config):
    df = env_config["df"]
    return StockTradingEnv(
        df=df,
        initial_balance=env_config.get("initial_balance", 10000),
        transaction_cost=env_config.get("transaction_cost", 0.001),
        window_size=env_config.get("window_size", 10),
    )


if __name__ == "__main__":
    ray.init(ignore_reinit_error=True)

    df = load_data()
    register_env("StockTradingEnv-v0", lambda config: env_creator({**config, "df": df}))

    tune.run(
        PPOTrainer,
        config={
            "env": "StockTradingEnv-v0",
            "framework": "torch",
            "env_config": {
                "df": df,
                "initial_balance": 10000,
                "transaction_cost": 0.001,
                "window_size": 10,
            },
            "num_workers": 1,
            "train_batch_size": 200,
            "sgd_minibatch_size": 64,
            "num_sgd_iter": 10,
            "lr": 1e-4,
            "gamma": 0.99,
            "model": {"fcnet_hiddens": [256, 256], "fcnet_activation": "relu"},
            "evaluation_interval": 1,
            "evaluation_num_episodes": 5,
            "evaluation_config": {"explore": False},
        },
        stop={"training_iteration": 20},
        checkpoint_at_end=True,
    )
