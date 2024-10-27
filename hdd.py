import io
import requests
import pandas as pd
import datetime

def get_stock_data(stock_symbol):
    # Construct the URL to get all historical data
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{stock_symbol}?period1=0&period2={int(datetime.datetime.now().timestamp())}&interval=1d&events=history&includeAdjustedClose=true'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Make the request to download the CSV data
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the data into a pandas DataFrame
        df = pd.read_csv(io.StringIO(response.text))
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        print(f"Error scraping {stock_symbol}: Failed to retrieve data. Status code: {response.status_code}")
        return None

def save_to_csv(df, stock_symbol):
    if df is not None:
        file_name = f'{stock_symbol}_historical_data.csv'
        df.to_csv(file_name, index=False)
        print(f'Data saved to {file_name}')
    else:
        print(f"No data to save for {stock_symbol}.")

if __name__ == "__main__":
    stock_symbols = ['A', 'AAL', 'AAP', 'AAPL']  # Add more symbols as needed
    for symbol in stock_symbols:
        try:
            df = get_stock_data(symbol)
            save_to_csv(df, symbol)
            print(f"Successfully scraped data for {symbol}")
        except Exception as e:
            print(f"Error scraping {symbol}: {e}")
