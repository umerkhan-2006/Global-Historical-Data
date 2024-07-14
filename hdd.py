import io
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json
import re

def get_stock_data(stock_symbol):
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{stock_symbol}?period1=0&period2={int(datetime.datetime.now().timestamp())}&interval=1d&events=history&includeAdjustedClose=true'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        raise ValueError(f"Failed to retrieve data. Status code: {response.status_code}")

def save_to_csv(df, stock_symbol):
    file_name = f'{stock_symbol}_historical_data.csv'
    df.to_csv(file_name, index=False)
    print(f'Data saved to {file_name}')

if __name__ == "__main__":
    stock_symbols = ['0001.HK', '0002.HK', '0003.HK', '0004.HK', '0005.HK', '0006.HK', '0008.HK', '0011.HK', '0012.HK', '0016.HK', '0017.HK', '0019.HK', '0023.HK', '0027.HK', '0066.HK', '0101.HK', '0388.HK', '0688.HK', '0700.HK', '0762.HK']  # Add more symbols as needed (HSI)
    for symbol in stock_symbols:
        try:
            df = get_stock_data(symbol)
            save_to_csv(df, symbol)
            print(f"Successfully scraped data for {symbol}")
        except ValueError as e:
            print(f"Error scraping {symbol}: {e}")