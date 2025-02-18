import gym
from gym import spaces
import numpy as np
import pandas as pd

class TradingEnv(gym.Env):
    def __init__(self, data, initial_capital=10000, trading_fee=0.001, look_back=50):
        super(TradingEnv, self).__init__()
        self.data = data
        self.initial_capital = initial_capital
        self.trading_fee = trading_fee
        self.look_back = look_back
        self.current_step = 0
        self.done = False

        # Define action and observation space
        self.action_space = spaces.Discrete(3)  # Buy, Sell, Hold
        self.observation_space = spaces.Box(low=0, high=1, shape=(look_back, 4), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        self.done = False
        self.current_capital = self.initial_capital
        self.position = 0
        return self._next_observation()

    def _next_observation(self):
        frame = np.array([
            self.data['price'].values[self.current_step:self.current_step + self.look_back],
            self.data['volume'].values[self.current_step:self.current_step + self.look_back],
            self.data['short_mavg'].values[self.current_step:self.current_step + self.look_back],
            self.data['long_mavg'].values[self.current_step:self.current_step + self.look_back]
        ])
        return frame.T

    def step(self, action):
        self._take_action(action)
        self.current_step += 1

        if self.current_step > len(self.data) - self.look_back:
            self.done = True

        reward = self._calculate_reward()
        obs = self._next_observation()
        return obs, reward, self.done, {}

    def _take_action(self, action):
        current_price = self.data['price'].values[self.current_step]
        if action == 0:  # Buy
            self.position += 1
            self.current_capital -= current_price * (1 + self.trading_fee)
        elif action == 1:  # Sell
            self.position -= 1
            self.current_capital += current_price * (1 - self.trading_fee)

    def _calculate_reward(self):
        current_price = self.data['price'].values[self.current_step]
        portfolio_value = self.current_capital + self.position * current_price
        return portfolio_value - self.initial_capital 