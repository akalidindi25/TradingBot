import pandas as pd
import numpy as np

class TrendFollower:
    def __init__(self, short_window=40, long_window=100):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['price']
        signals['short_mavg'] = data['price'].rolling(window=self.short_window, min_periods=1).mean()
        signals['long_mavg'] = data['price'].rolling(window=self.long_window, min_periods=1).mean()
        signals['signal'] = 0.0
        signals.loc[self.short_window:, 'signal'] = np.where(
            signals['short_mavg'][self.short_window:] > signals['long_mavg'][self.short_window:], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()
        return signals 