import yfinance as yf
import pandas as pd
import logging
from .config import DEFAULT_STOCK_TICKERS

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_stock_data(tickers=DEFAULT_STOCK_TICKERS):
    logging.info(f"Starting fetch for stock data: {tickers}")
    try:
        data = yf.download(tickers, period='1d', interval='1m')
        stocks = []
        
        for ticker in tickers:
            stock_info = data['Close'][ticker].iloc[-1]
            day_high = data['High'][ticker].max()
            day_low = data['Low'][ticker].min()
            stocks.append({
                'ticker': ticker,
                'current_price': stock_info,
                'day_high': day_high,
                'day_low': day_low
            })
        
        df = pd.DataFrame(stocks)
        logging.info("Successfully fetched and processed stock data")
        return df
    except Exception as e:
        logging.error(f"Error fetching stock data: {e}")
        return pd.DataFrame()

def fetch_historical_stock_data(tickers=DEFAULT_STOCK_TICKERS, period='1y'):
    try:
        data = yf.download(tickers, period=period, interval='1d')
        data.reset_index(inplace=True)
        data.rename(columns={'Date': 'timestamp', 'Close': 'price', 'Volume': 'volume'}, inplace=True)
        logging.info("Successfully fetched historical stock data.")
        return data[['timestamp', 'price', 'volume']]
    except Exception as e:
        logging.error(f"Error fetching historical stock data: {e}")
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    print(fetch_stock_data()) 