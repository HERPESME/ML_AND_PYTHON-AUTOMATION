# tests/test_rl_agent.py

import unittest
import numpy as np
from src.rl_agent.dqn_agent import DQNAgent  # Corrected import path


class TestDQNAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DQNAgent(state_size=10, action_size=3)

    def test_act_returns_valid_action(self):
        state = np.random.rand(10)
        action = self.agent.act(state)
        self.assertIn(action, [0, 1, 2], "Action must be one of [0, 1, 2]")

    def test_remember_stores_experience(self):
        initial_memory_length = len(self.agent.memory)
        self.agent.remember(np.zeros(10), 1, 0.0, np.zeros(10), False)
        self.assertEqual(
            len(self.agent.memory),
            initial_memory_length + 1,
            "Experience should be added to memory",
        )

    def test_replay_does_not_crash(self):
        for _ in range(32):
            self.agent.remember(np.zeros(10), 1, 0.0, np.zeros(10), False)
        try:
            self.agent.replay(batch_size=32)
        except Exception as e:
            self.fail(f"Replay crashed with exception: {e}")


if __name__ == "__main__":
    unittest.main()
