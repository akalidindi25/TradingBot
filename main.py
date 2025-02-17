import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.fetch_crypto import fetch_top_cryptos
from api.fetch_stocks import fetch_stock_data
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
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