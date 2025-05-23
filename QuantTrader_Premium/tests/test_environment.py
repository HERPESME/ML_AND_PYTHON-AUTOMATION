# Python file
import pytest
import gymnasium as gym
from src.env.stock_trading_env import StockTradingEnv
import numpy as np


def test_environment_reset():
    env = StockTradingEnv()
    obs, info = env.reset()
    assert isinstance(obs, np.ndarray)
    assert obs.shape[0] > 0


def test_environment_step():
    env = StockTradingEnv()
    obs, info = env.reset()
    action = env.action_space.sample()  # random action (0 = sell, 1 = hold, 2 = buy)
    new_obs, reward, done, truncated, info = env.step(action)
    assert isinstance(new_obs, np.ndarray)
    assert isinstance(reward, float)
    assert isinstance(done, bool)
    assert isinstance(truncated, bool)


def test_action_space():
    env = StockTradingEnv()
    assert env.action_space.n == 3


def test_observation_space():
    env = StockTradingEnv()
    assert isinstance(env.observation_space.shape, tuple)
    assert env.observation_space.shape[0] > 0
