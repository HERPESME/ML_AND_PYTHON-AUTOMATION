# Python file
import os
import pandas as pd
import numpy as np
import torch
from ray.rllib.agents.ppo import PPOTrainer
from ray.tune.registry import register_env
from src.env.stock_trading_env import StockTradingEnv
from dotenv import load_dotenv

load_dotenv()


def load_data():
    data_path = os.path.join("data", "historical", "AAPL.csv")
    df = pd.read_csv(data_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def env_creator(env_config):
    df = env_config["df"]
    return StockTradingEnv(df=df)


def evaluate_agent(agent, env):
    obs = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = agent.compute_single_action(obs, explore=False)
        obs, reward, done, _ = env.step(action)
        env.render()
        total_reward += reward

    print(f"Total Profit: {env.net_worth - env.initial_balance:.2f}")
    return total_reward


if __name__ == "__main__":
    df = load_data()
    register_env("StockTradingEnv-v0", lambda config: env_creator({**config, "df": df}))

    env = StockTradingEnv(df=df)

    checkpoint_path = os.getenv("CHECKPOINT_PATH", "checkpoints/PPO/checkpoint")
    agent = PPOTrainer(env="StockTradingEnv-v0")
    agent.restore(checkpoint_path)

    evaluate_agent(agent, env)
