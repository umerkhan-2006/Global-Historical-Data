import io
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def get_stock_data(stock_symbol):
    # Set start and end dates for the full range (you can change these if needed)
    start_date = "0"  # January 1, 1970
    end_date = int(datetime.datetime.now().timestamp())  # Current timestamp

    # Yahoo Finance historical data URL
    url = f'https://finance.yahoo.com/quote/{stock_symbol}/history?p={stock_symbol}&period1={start_date}&period2={end_date}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Look for the correct table by class name
        table = soup.find('table', {'class': 'W(100%) M(0)'})  # Check the page for the exact class name

        if table is not None:
            rows = table.find_all('tr')
            data = []

            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if len(cols) > 0:
                    data.append([col.text for col in cols])

            # Create a DataFrame
            df = pd.DataFrame(data, columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        else:
            print(f"Error scraping {stock_symbol}: No historical data table found. Check if the symbol is correct or if data is available.")
            return pd.DataFrame()  # Return an empty DataFrame instead of None
    else:
        print(f"Error scraping {stock_symbol}: Failed to retrieve data. Status code: {response.status_code}")
        return pd.DataFrame()  # Return an empty DataFrame instead of None

def save_to_csv(df, stock_symbol):
    if not df.empty:  # Check if DataFrame is not empty
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
