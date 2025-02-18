import requests
import pandas as pd
import logging
from .config import COINGECKO_API_URL
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Simple in-memory cache
cache = {}
cache_expiry = timedelta(minutes=10)  # Cache expiry time

def fetch_top_cryptos():
    logging.info("Starting fetch for top cryptocurrencies")
    try:
        response = requests.get(f"{COINGECKO_API_URL}/coins/markets", params={
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': False
        })
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant data
        cryptos = [{
            'symbol': item['symbol'],
            'current_price': item['current_price'],
            '24h_change': item['price_change_percentage_24h'],
            'market_cap': item['market_cap']
        } for item in data]
        
        # Convert to DataFrame
        df = pd.DataFrame(cryptos)
        logging.info("Successfully fetched and processed cryptocurrency data")
        return df
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching cryptocurrency data: {e}")
        return pd.DataFrame()

def fetch_historical_crypto_data(coin_id='bitcoin', days=365):
    try:
        # Check if data is in cache and not expired
        if coin_id in cache and datetime.now() - cache[coin_id]['timestamp'] < cache_expiry:
            logging.info("Using cached data for historical cryptocurrency data.")
            logging.debug(f"Cached data: {cache[coin_id]['data'].head()}")
            return cache[coin_id]['data']

        response = requests.get(f"{COINGECKO_API_URL}/coins/{coin_id}/market_chart", params={
            'vs_currency': 'usd',
            'days': days
        })
        response.raise_for_status()
        data = response.json()
        
        # Convert to DataFrame
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['volume'] = [v[1] for v in data['total_volumes']]
        logging.info("Successfully fetched historical cryptocurrency data.")

        # Cache the data
        cache[coin_id] = {'data': df, 'timestamp': datetime.now()}
        logging.debug(f"Newly fetched data: {df.head()}")
        return df
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching historical cryptocurrency data: {e}")
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    print(fetch_top_cryptos()) 