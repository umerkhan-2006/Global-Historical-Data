import io
import requests
import pandas as pd
import datetime
import time

def get_stock_data(stock_symbol):
    end_date = int(datetime.datetime.now().timestamp())
    start_date = int((datetime.datetime.now() - datetime.timedelta(days=365)).timestamp())
    
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{stock_symbol}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        print(f"Response text: {response.text}")  # Debugging line
        raise ValueError(f"Failed to retrieve data. Status code: {response.status_code}")

def save_to_csv(df, stock_symbol):
    file_name = f'{stock_symbol}_historical_data.csv'
    df.to_csv(file_name, index=False)
    print(f'Data saved to {file_name}')

if __name__ == "__main__":
    stock_symbols = ['A', 'AAL', 'AAP', 'AAPL']  # Add more symbols as needed
    for symbol in stock_symbols:
        try:
            df = get_stock_data(symbol)
            save_to_csv(df, symbol)
            print(f"Successfully scraped data for {symbol}")
        except ValueError as e:
            print(f"Error scraping {symbol}: {e}")
            time.sleep(1)  # Sleep for 1 second between requests
