import sqlite3
from config import *

connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock(
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL UNIQUE,
    company TEXT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price(
        id INTEGER PRIMARY KEY,
        stock_id INTEGER,
        date NOT null,
        open not null,
        high not null,
        low not null,
        close not null,
        adjusted_close not null,
        volume not null,
        FOREIGN KEY (stock_id) REFERENCES stock(id)
    );

""")


connection.commit()