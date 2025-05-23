import numpy as np
import random
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam

# Import config constants
from src.utils.config import STATE_SIZE, ACTION_SIZE, EPSILON_DECAY


class DQNAgent:
    def __init__(self):
        self.state_size = STATE_SIZE
        self.action_size = ACTION_SIZE
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = EPSILON_DECAY
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential(
            [
                Input(shape=(self.state_size,)),
                Dense(24, activation="relu"),
                Dense(24, activation="relu"),
                Dense(self.action_size, activation="linear"),
            ]
        )
        model.compile(loss="mse", optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(np.array([state]), verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size=32):
        minibatch = random.sample(self.memory, min(len(self.memory), batch_size))
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_q = self.model.predict(np.array([next_state]), verbose=0)[0]
                target += self.gamma * np.amax(next_q)
            target_f = self.model.predict(np.array([state]), verbose=0)
            target_f[0][action] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def decide_action(self, anomalies):
        """
        Convert anomalies into a numerical state vector and return an action.
        Dummy: [#anomalies, average score]
        """
        scores = [a.get("score", 0) for a in anomalies]
        avg_score = np.mean(scores) if scores else 0
        state = np.array([len(anomalies), avg_score])
        if len(state) < self.state_size:
            state = np.pad(state, (0, self.state_size - len(state)))
        return self.act(state[: self.state_size])
