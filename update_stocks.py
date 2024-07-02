import sqlite3
import alpaca_trade_api as tradeapi
import logging
from config import *
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

# Set up logging
logging.basicConfig(filename=LOGFILE_PATH, 
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info('Starting update stocks script')

    # Establish a connection to the database
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Fetch all symbols and companies from the stock table
        cursor.execute("SELECT symbol, company FROM stock")
        rows = cursor.fetchall()
        symbols = [row['symbol'] for row in rows]
        companies = [row['company'] for row in rows]

        trading_client = TradingClient(API_KEY, API_SECRET_KEY)

        # search for crypto assets
        search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)

        assets = trading_client.get_all_assets(search_params)
        print(assets)

        # Iterate over the assets and insert the active and tradable ones into the stock table
        for asset in assets:
            try:
                if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
                    logging.info(f"Adding new stock: {asset.symbol} {asset.name}")
                    cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
            except Exception as e:
                logging.error(f"Error with asset {asset.symbol}: {e}")

        # Commit the transaction and close the connection
        connection.commit()
        logging.info('Stock update completed successfully')

    except Exception as e:
        logging.error(f"Error in main function: {e}")

    finally:
        if connection:
            connection.close()
            logging.info('Database connection closed')

if __name__ == "__main__":
    main()
