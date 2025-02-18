class TradingAgent:
    def __init__(self, initial_capital=10000, trading_fee=0.001):
        self.initial_capital = initial_capital
        self.trading_fee = trading_fee
        self.current_capital = initial_capital
        self.position = 0  # Positive for long, negative for short

    def buy(self, price, quantity):
        cost = price * quantity * (1 + self.trading_fee)
        if self.current_capital >= cost:
            self.current_capital -= cost
            self.position += quantity
            return True
        return False

    def sell(self, price, quantity):
        if self.position >= quantity:
            revenue = price * quantity * (1 - self.trading_fee)
            self.current_capital += revenue
            self.position -= quantity
            return True
        return False

    def get_portfolio_value(self, current_price):
        return self.current_capital + self.position * current_price 