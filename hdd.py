import os  # This imports the operating system module to check directories
print("Current directory:", os.getcwd())  # This will print the current directory path

import io
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def fetch_yahoo_crumb_and_cookie(stock_symbol):
    """
    Function to fetch crumb and cookie required for Yahoo Finance request.
    """
    url = f'https://finance.yahoo.com/quote/{stock_symbol}/history?p={stock_symbol}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    cookie = response.cookies['B']  # Cookie needed for request

    # Scraping the crumb
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find("script", text=lambda t: "CrumbStore" in t).text
    crumb = script.split('"CrumbStore":{"crumb":"')[1].split('"}')[0]

    return crumb, cookie

def get_stock_data(stock_symbol):
    """
    Function to retrieve historical stock data from Yahoo Finance.
    """
    try:
        crumb, cookie = fetch_yahoo_crumb_and_cookie(stock_symbol)
    except Exception as e:
        print(f"Failed to retrieve crumb and cookie for {stock_symbol}: {e}")
        return None

    url = f'https://query1.finance.yahoo.com/v7/finance/download/{stock_symbol}'
    params = {
        'period1': 0,
        'period2': int(datetime.datetime.now().timestamp()),
        'interval': '1d',
        'events': 'history',
        'crumb': crumb
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': f'B={cookie}'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        print(f"Error scraping {stock_symbol}: Failed to retrieve data. Status code: {response.status_code}")
        return None

def save_to_csv(df, stock_symbol):
    file_name = f'{stock_symbol}_historical_data.csv'
    df.to_csv(file_name, index=False)
    print(f'Data saved to {file_name}')

if __name__ == "__main__":
    stock_symbols = ['A', 'AAL', 'AAP', 'AAPL']
    for symbol in stock_symbols:
        df = get_stock_data(symbol)
        if df is not None:
            save_to_csv(df, symbol)
            print(f"Successfully scraped data for {symbol}")
        else:
            print(f"No data to save for {symbol}")
