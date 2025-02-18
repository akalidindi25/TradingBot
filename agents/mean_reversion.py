import pandas as pd
import numpy as np

class MeanReversion:
    def __init__(self, window=20, threshold=1.5):
        self.window = window
        self.threshold = threshold

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['price']
        signals['mean'] = data['price'].rolling(window=self.window, min_periods=1).mean()
        signals['std'] = data['price'].rolling(window=self.window, min_periods=1).std()
        signals['z_score'] = (signals['price'] - signals['mean']) / signals['std']
        signals['signal'] = np.where(signals['z_score'] > self.threshold, -1.0, 0.0)
        signals['signal'] = np.where(signals['z_score'] < -self.threshold, 1.0, signals['signal'])
        signals['positions'] = signals['signal'].diff()
        signals['buy_signal'] = signals['signal'] == 1.0
        signals['sell_signal'] = signals['signal'] == -1.0
        return signals 