from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient ,CryptoHistoricalDataClient

from alpaca.data.requests import StockLatestBarRequest
from alpaca.data.requests import StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from config import *

trading_client = TradingClient(API_KEY, API_SECRET_KEY)
stock_client = StockHistoricalDataClient(API_KEY,API_SECRET_KEY)

stock_request_params = StockBarsRequest(
                        symbol_or_symbols=["AAPL", "MSFT"],
                        timeframe=TimeFrame.Day,
                        start=datetime(2024, 6, 25),
                        end=datetime(2024, 6, 28)
                 )

stock_bars = stock_client.get_stock_bars(stock_request_params)
print(stock_bars)

for symbol in stock_bars.data:
    print(f"Processing symbol {symbol}")
    for bar in stock_bars.data[symbol]:
        print(bar.timestamp,bar.open,bar.high,bar.low,bar.close,bar.volume)
        
  