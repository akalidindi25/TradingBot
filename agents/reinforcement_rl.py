import os
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from agents.trading_environment import TradingEnv

class ReinforcementRL:
    def __init__(self, data, model_path='models/rl_model.zip'):
        self.data = data
        self.model_path = model_path
        self.env = DummyVecEnv([lambda: TradingEnv(data)])
        self.model = PPO('MlpPolicy', self.env, verbose=1)

    def train(self, timesteps=10000):
        self.model.learn(total_timesteps=timesteps)
        self.model.save(self.model_path)

    def evaluate(self):
        obs = self.env.reset()
        for _ in range(len(self.data)):
            action, _states = self.model.predict(obs)
            obs, rewards, done, info = self.env.step(action)
            if done:
                break

# Example usage
if __name__ == "__main__":
    # Load your data here
    data = pd.read_csv('path_to_your_data.csv')
    data = calculate_moving_averages(data)  # Ensure moving averages are calculated
    rl_agent = ReinforcementRL(data)
    rl_agent.train()
    rl_agent.evaluate() 