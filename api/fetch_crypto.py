import requests
import pandas as pd
import logging
from .config import COINGECKO_API_URL

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

# Example usage
if __name__ == "__main__":
    print(fetch_top_cryptos()) 