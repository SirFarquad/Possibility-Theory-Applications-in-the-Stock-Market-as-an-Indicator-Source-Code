import yfinance as yf
import sqlite3
import pandas as pd

# Fetch historical SPY data from Yahoo Finance
def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data['Ticker'] = ticker
    return data

# Create a table to store the data
def create_table(db_name='stock_data.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_prices (
        Date TEXT PRIMARY KEY,
        SPY_Close REAL,
        Leverage_Close REAL
    )
    ''')
    conn.commit()
    conn.close()

# Insert or update the data into the database
def store_data(spy_data, leverage_data, db_name='stock_data.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Merge SPY and leverage data on the date
    combined_data = pd.merge(spy_data[['Close']], leverage_data[['Close']],
                             left_index=True, right_index=True, 
                             how='outer', suffixes=('_SPY', '_Leverage'))

    combined_data.index = combined_data.index.strftime('%Y-%m-%d')

    for date, row in combined_data.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO stock_prices 
            (Date, SPY_Close, Leverage_Close) 
            VALUES (?, ?, ?)
        ''', (date, row['Close_SPY'], row['Close_Leverage']))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    spy_data = fetch_data('SPY', '2000-01-01', '2024-01-01')
    leverage_data = fetch_data('SSO', '2007-04-01', '2024-01-01')

    store_data(spy_data, leverage_data)
