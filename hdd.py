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
    stock_symbols = ['3IN.L', 'AAL.L', 'ABF.L', 'ADM.L', 'AHT.L', 'ANTO.L', 'AUTO.L', 'AV.L', 'AZN.L', 'BA.L', 'BARC.L', 'BATS.L', 'BDEV.L', 'BKG.L', 'BLND.L', 'BME.L', 'BNZL.L', 'BP.L', 'BRBY.L', 'BT-A.L', 'CCH.L', 'CPG.L', 'CRH.L', 'CRDA.L', 'DCC.L', 'DGE.L', 'DLG.L', 'EXPN.L', 'FERG.L', 'FLTR.L', 'GLEN.L', 'GSK.L', 'HLMA.L', 'HSBA.L', 'IAG.L', 'ICP.L', 'IHG.L', 'III.L', 'IMB.L', 'INF.L', 'ITRK.L', 'JD.L', 'JET.L', 'KGF.L', 'LAND.L', 'LGEN.L', 'LLOY.L', 'LSE.L', 'MNDI.L', 'MNG.L', 'MRO.L', 'MRW.L', 'NG.L', 'NXT.L', 'OCDO.L', 'PHNX.L', 'POLY.L', 'PRU.L', 'PSN.L', 'PSON.L', 'RB.L', 'RDSA.L', 'RDSB.L', 'REL.L', 'RIO.L', 'RR.L', 'RTO.L', 'SBRY.L', 'SDR.L', 'SGE.L', 'SGRO.L', 'SHEL.L', 'SMDS.L', 'SMIN.L', 'SMT.L', 'SN.L', 'SPX.L', 'SSE.L', 'STAN.L', 'STJ.L', 'SVT.L', 'TSCO.L', 'TW.L', 'ULVR.L', 'UU.L', 'VOD.L', 'WEIR.L', 'WTB.L', 'WPP.L']  # Add more symbols as needed (FTSE 100)
    for symbol in stock_symbols:
        try:
            df = get_stock_data(symbol)
            save_to_csv(df, symbol)
            print(f"Successfully scraped data for {symbol}")
        except ValueError as e:
            print(f"Error scraping {symbol}: {e}")