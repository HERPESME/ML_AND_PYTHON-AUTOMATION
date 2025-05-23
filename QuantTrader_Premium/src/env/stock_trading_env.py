# Python file
import gym
import numpy as np


class StockTradingEnv(gym.Env):
    def __init__(
        self, df, initial_balance=10000, transaction_cost=0.001, window_size=10
    ):
        super(StockTradingEnv, self).__init__()

        self.df = df.reset_index(drop=True)
        self.initial_balance = initial_balance
        self.transaction_cost = transaction_cost
        self.window_size = window_size
        self.current_step = self.window_size

        self.action_space = gym.spaces.Discrete(3)  # 0: hold, 1: buy, 2: sell
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(window_size, 5), dtype=np.float32
        )

        self.reset()

    def reset(self):
        self.balance = self.initial_balance
        self.shares_held = 0
        self.net_worth = self.initial_balance
        self.max_net_worth = self.initial_balance
        self.trades = []
        self.current_step = self.window_size
        return self._get_observation()

    def _get_observation(self):
        obs = self.df.iloc[self.current_step - self.window_size : self.current_step][
            ["Open", "High", "Low", "Close", "Volume"]
        ].values
        return obs

    def step(self, action):
        current_price = self.df.iloc[self.current_step]["Close"]

        reward = 0
        done = False

        if action == 1:  # Buy
            max_shares = self.balance // current_price
            if max_shares > 0:
                self.shares_held += max_shares
                cost = max_shares * current_price * (1 + self.transaction_cost)
                self.balance -= cost
                self.trades.append(("buy", self.current_step, current_price))

        elif action == 2:  # Sell
            if self.shares_held > 0:
                proceeds = (
                    self.shares_held * current_price * (1 - self.transaction_cost)
                )
                self.balance += proceeds
                self.shares_held = 0
                self.trades.append(("sell", self.current_step, current_price))

        self.net_worth = self.balance + self.shares_held * current_price
        self.max_net_worth = max(self.max_net_worth, self.net_worth)

        reward = self.net_worth - self.initial_balance
        self.current_step += 1

        if self.current_step >= len(self.df):
            done = True

        return self._get_observation(), reward, done, {}

    def render(self, mode="human"):
        profit = self.net_worth - self.initial_balance
        print(
            f"Step: {self.current_step}, Balance: {self.balance:.2f}, Shares held: {self.shares_held}, Net worth: {self.net_worth:.2f}, Profit: {profit:.2f}"
        )
