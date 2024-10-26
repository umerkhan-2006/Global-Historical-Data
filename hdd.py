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
        # Use BeautifulSoup to parse the page and extract the data table
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'data-test': 'historical-prices'})  # Look for the correct table

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
            raise ValueError("No historical data table found.")
    else:
        raise ValueError(f"Failed to retrieve data. Status code: {response.status_code}")


def save_to_csv(df, stock_symbol):
    file_name = f'{stock_symbol}_historical_data.csv'
    df.to_csv(file_name, index=False)
    print(f'Data saved to {file_name}')

if __name__ == "__main__":
    stock_symbols = ['A', 'AAL', 'AAP', 'AAPL']  # Add more symbols as needed (ALL)
    for symbol in stock_symbols:
        try:
            df = get_stock_data(symbol)
            save_to_csv(df, symbol)
            print(f"Successfully scraped data for {symbol}")
        except ValueError as e:
            print(f"Error scraping {symbol}: {e}")
