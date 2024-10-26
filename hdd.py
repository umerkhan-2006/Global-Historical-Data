import io
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def get_stock_data(stock_symbol):
    # Set a very early period1 to capture all historical data
    period1 = 0  # Start from January 1, 1970
    period2 = int(datetime.datetime.now().timestamp())  # Current time

    # Use the Yahoo Finance historical data page for scraping
    url = f'https://finance.yahoo.com/quote/{stock_symbol}/history?p={stock_symbol}&period1={period1}&period2={period2}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Use BeautifulSoup to parse the HTML and extract data
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'data-test': 'historical-prices'})  # Find the historical prices table
        rows = table.find_all('tr')

        data = []
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) > 0:
                date = cols[0].text
                open_price = cols[1].text
                high = cols[2].text
                low = cols[3].text
                close = cols[4].text
                adj_close = cols[5].text
                volume = cols[6].text
                data.append([date, open_price, high, low, close, adj_close, volume])

        # Convert the list to a DataFrame
        df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        df['Date'] = pd.to_datetime(df['Date'])
        return df
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
