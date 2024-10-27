import pandas as pd
import os

def load_data(symbol):
    file_path = f'{str(symbol)}_historical_data.csv'
    if os.path.exists(file_path):
        return pd.read_csv(file_path, index_col='Date', parse_dates=True)
    else:
        print(f"File {file_path} not found.")
        return None

# List of symbols
symbols = [
    'A', 'AAL', 'AAP', 'AAPL'
    ]

# Load data for each symbol
for symbol in symbols:
    data = load_data(symbol)
    if data is not None:
        print(f"Loaded data for {symbol}")
    else:
        print(f"Data for {symbol} could not be loaded.")