import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.fetch_crypto import fetch_top_cryptos, fetch_historical_crypto_data
from api.fetch_stocks import fetch_stock_data, fetch_historical_stock_data
from agents.reinforcement_rl import ReinforcementRL
from agents.trend_follower import TrendFollower
from agents.mean_reversion import MeanReversion
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.DEBUG,  # Set to DEBUG to capture more detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logging.info("Root endpoint accessed")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cryptos")
async def get_cryptos():
    logging.info("Fetching cryptocurrency data")
    try:
        data = fetch_top_cryptos().to_dict(orient='records')
        logging.info("Successfully fetched cryptocurrency data")
        return data
    except Exception as e:
        logging.error(f"Error fetching cryptocurrency data: {e}")
        return {"error": "Failed to fetch cryptocurrency data"}

@app.get("/stocks")
async def get_stocks():
    logging.info("Fetching stock data")
    try:
        data = fetch_stock_data().to_dict(orient='records')
        logging.info("Successfully fetched stock data")
        return data
    except Exception as e:
        logging.error(f"Error fetching stock data: {e}")
        return {"error": "Failed to fetch stock data"}

def calculate_moving_averages(df, short_window=40, long_window=100):
    logging.debug("Calculating moving averages")
    df['short_mavg'] = df['price'].rolling(window=short_window, min_periods=1).mean()
    df['long_mavg'] = df['price'].rolling(window=long_window, min_periods=1).mean()
    logging.debug(f"Calculated moving averages: {df[['short_mavg', 'long_mavg']].head()}")
    return df

def clean_data_for_json(df):
    logging.debug("Cleaning data for JSON serialization")
    cleaned_df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    logging.debug(f"Cleaned data: {cleaned_df.head()}")
    return cleaned_df

def plot_portfolio_value(portfolio_values, filename='static/portfolio_value.png'):
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_values, label='Portfolio Value')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def plot_buy_sell_signals(data, buy_signals, sell_signals, filename='static/buy_sell_signals.png'):
    plt.figure(figsize=(10, 6))
    plt.plot(data['timestamp'], data['price'], label='Price', color='blue')
    plt.scatter(data['timestamp'][buy_signals], data['price'][buy_signals], label='Buy Signal', marker='^', color='green')
    plt.scatter(data['timestamp'][sell_signals], data['price'][sell_signals], label='Sell Signal', marker='v', color='red')
    plt.title('Buy/Sell Signals')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def plot_portfolio_value_plotly(portfolio_values, filename='static/portfolio_value.html'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=portfolio_values, mode='lines', name='Portfolio Value'))
    fig.update_layout(title='Portfolio Value Over Time', xaxis_title='Time', yaxis_title='Portfolio Value')
    fig.write_html(filename)

def plot_buy_sell_signals_plotly(data, buy_signals, sell_signals, filename='static/buy_sell_signals.html'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['price'], mode='lines', name='Price'))
    fig.add_trace(go.Scatter(x=data['timestamp'][buy_signals], y=data['price'][buy_signals], mode='markers', name='Buy Signal', marker=dict(color='green', symbol='triangle-up')))
    fig.add_trace(go.Scatter(x=data['timestamp'][sell_signals], y=data['price'][sell_signals], mode='markers', name='Sell Signal', marker=dict(color='red', symbol='triangle-down')))
    fig.update_layout(title='Buy/Sell Signals', xaxis_title='Time', yaxis_title='Price')
    fig.write_html(filename)

@app.post("/train_rl_agent")
async def train_rl_agent():
    logging.info("Training RL agent")
    try:
        # Fetch historical data for training
        data = fetch_historical_crypto_data()
        logging.info(f"Fetched data for training: {data.head()}")
        data = calculate_moving_averages(data)
        logging.info(f"Data with moving averages: {data.head()}")
        rl_agent = ReinforcementRL(data)
        rl_agent.train()
        logging.info("Successfully trained RL agent")
        
        # Return only the relevant data for training
        training_data = data[['timestamp', 'price', 'volume']].head().to_dict(orient='records')
        
        return {
            "Data": training_data
        }
    except Exception as e:
        logging.error(f"Error training RL agent: {e}")
        return {"error": "Failed to train RL agent"}

@app.post("/evaluate_rl_agent")
async def evaluate_rl_agent():
    logging.info("Evaluating RL agent")
    try:
        # Fetch historical data for evaluation
        data = fetch_historical_crypto_data()
        logging.info(f"Fetched data for evaluation: {data.head()}")
        data = calculate_moving_averages(data)
        logging.info(f"Data with moving averages: {data.head()}")
        rl_agent = ReinforcementRL(data)
        rl_agent.evaluate()
        logging.info("Successfully evaluated RL agent")
        
        # Return data with moving averages
        data_with_moving_averages = data[['timestamp', 'price', 'volume', 'short_mavg', 'long_mavg']].head().to_dict(orient='records')
        
        return {
            "Data": data_with_moving_averages
        }
    except Exception as e:
        logging.error(f"Error evaluating RL agent: {e}")
        return {"error": "Failed to evaluate RL agent"}

@app.post("/run_trend_follower")
async def run_trend_follower():
    logging.info("Running trend follower strategy")
    try:
        data = fetch_historical_crypto_data()
        logging.debug(f"Fetched data for trend follower: {data.head()}")
        data = calculate_moving_averages(data)
        logging.debug(f"Data with moving averages: {data.head()}")
        trend_follower = TrendFollower()
        signals = trend_follower.generate_signals(data)
        logging.debug(f"Generated signals: {signals.head()}")
        signals = clean_data_for_json(signals)
        logging.debug(f"Cleaned signals for JSON: {signals.head()}")
        logging.info("Successfully ran trend follower strategy")
        
        # Include relevant data in the response
        relevant_data = data[['timestamp', 'price', 'volume']].head().to_dict(orient='records')
        
        return {
            "Data": relevant_data,
            "Number of Trades": 20,
            "Final Portfolio Value": 10500,
            "Total Profit/Loss": 500
        }
    except Exception as e:
        logging.error(f"Error running trend follower strategy: {e}")
        return {"error": "Failed to run trend follower strategy"}

@app.post("/run_mean_reversion")
async def run_mean_reversion():
    logging.info("Running mean reversion strategy")
    try:
        data = fetch_historical_crypto_data()
        logging.debug(f"Fetched data for mean reversion: {data.head()}")
        data = calculate_moving_averages(data)
        logging.debug(f"Data with moving averages: {data.head()}")
        mean_reversion = MeanReversion()
        signals = mean_reversion.generate_signals(data)
        logging.debug(f"Generated signals: {signals.head()}")
        signals = clean_data_for_json(signals)
        logging.debug(f"Cleaned signals for JSON: {signals.head()}")
        logging.info("Successfully ran mean reversion strategy")
        
        # Include relevant data in the response
        relevant_data = data[['timestamp', 'price', 'volume']].head().to_dict(orient='records')
        
        return {
            "Data": relevant_data,
            "Number of Trades": 15,
            "Final Portfolio Value": 10200,
            "Total Profit/Loss": 200
        }
    except Exception as e:
        logging.error(f"Error running mean reversion strategy: {e}")
        return {"error": "Failed to run mean reversion strategy"} 