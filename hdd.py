import os
import yfinance as yf
import pandas as pd

# Check the current directory
print("Current directory:", os.getcwd())

def get_stock_data(stock_symbol):
    # Download stock data using yfinance
    stock_data = yf.download(stock_symbol, start="1900-01-01", end="2024-01-01", interval="1d")
    return stock_data

def save_to_csv(df, stock_symbol):
    file_name = f'{stock_symbol}_historical_data.csv'
    df.to_csv(file_name)
    print(f'Data saved to {file_name}')

if __name__ == "__main__":
    stock_symbols = ['A', 'AAL', 'AAP', 'AAPL']
    for symbol in stock_symbols:
        df = get_stock_data(symbol)
        if not df.empty:
            save_to_csv(df, symbol)
            print(f"Successfully scraped data for {symbol}")
        else:
            print(f"No data to save for {symbol}")
