# TradingBot Web Application

TradingBot is a web application designed to fetch and analyze live cryptocurrency and stock prices. It uses FastAPI for the web framework and Uvicorn as the ASGI server to provide real-time data and insights for traders and developers.

## Features

- **Cryptocurrency Data Fetching**: Uses the CoinGecko API to fetch the top 10 cryptocurrencies by market cap, including details like symbol, current price, 24-hour change, and market cap.
- **Stock Data Fetching**: Utilizes the yfinance library to retrieve real-time stock prices, including current price, day's high, and day's low for specified tickers.
- **Web Interface**: Provides a RESTful API to access cryptocurrency and stock data.

## Folder Structure

- `api/`: Contains scripts and configuration for fetching data.
  - `fetch_crypto.py`: Script for fetching cryptocurrency data.
  - `fetch_stocks.py`: Script for fetching stock data.
  - `config.py`: Configuration file for API endpoints and default stock tickers.
- `static/`: Contains static files like CSS and JavaScript.
- `templates/`: Contains HTML templates for the web interface.
- `logs/`: Directory where log files are stored.
- `main.py`: The main entry point for the FastAPI application.
- `requirements.txt`: Lists the dependencies required for the project.

## Setup Instructions

1. **Clone the Repository**

   Clone the repository to your local machine using:

   ```bash
   git clone <repository-url>
   cd TradingBot
   ```

2. **Install Dependencies**

   Install the required Python libraries using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

   The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

- **GET /cryptos**: Fetches the top 10 cryptocurrencies by market cap.
- **GET /stocks**: Fetches real-time stock prices for default tickers.

## Configuration

- Modify `api/config.py` to change API URLs or default stock tickers.
- Use environment variables for sensitive configurations if needed.

## Logging

The project includes detailed logging for successful API calls and errors. Logs are written to `logs/app.log` for easy debugging and monitoring. Ensure the `logs` directory exists to capture log files.

## Documentation

Each function in the scripts is documented with docstrings. You can view these by inspecting the code or using tools like `pydoc`.

## Error Handling

The application includes error handling to manage exceptions during data fetching. Errors are logged, and a user-friendly error message is returned by the API.
