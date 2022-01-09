import csv
import io
import requests
import pandas as pd
import time

API_KEY_1 = 'ZI2FIPRUVTWAT4BK'
API_KEY_2 = 'NNG7F7YS6OBDZF4Q'
# symbol = 'SPY'
# slice = 'year1month1'

def downloadQuotes(symbol, slice):
    CSV_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={symbol}&interval=5min&slice={slice}&apikey={API_KEY_1}'

    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        if 'Thank you for using Alpha Vantage!' in decoded_content:
            return
        if len(decoded_content) < 100:
            print(f"response is empty for {symbol}")
            return
        df = pd.read_csv(io.StringIO(decoded_content), sep=",")
        print(df)
        print(len(df))
        df.to_csv(f'quotes/{symbol}-{slice}.csv', index=False)

def downloadForex(fromSymbol, toSymbol, slice):
    CSV_URL = f'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={fromSymbol}&to_symbol={toSymbol}&outputsize=full&interval=5min&slice={slice}&apikey={API_KEY_1}&datatype=csv'

    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        if 'Thank you for using Alpha Vantage!' in decoded_content:
            return
        if len(decoded_content) < 100:
            print(f"response is empty for {fromSymbol} => {toSymbol}")
            return
        df = pd.read_csv(io.StringIO(decoded_content), sep=",")
        print(df)
        print(len(df))
        df.to_csv(f'quotes/{fromSymbol}{toSymbol}-{slice}.csv', index=False)

def getAllSymbols():
    symbol_urls = [
        'https://raw.githubusercontent.com/hairinwind/pyahoo/master/config/symbol.1.txt', 
        'https://raw.githubusercontent.com/hairinwind/pyahoo/master/config/symbol.2.txt',
        'https://raw.githubusercontent.com/hairinwind/pyahoo/master/config/symbol.3.txt',
        'https://raw.githubusercontent.com/hairinwind/pyahoo/master/config/symbol.4.txt',
        'https://raw.githubusercontent.com/hairinwind/pyahoo/master/config/symbol.5.txt'
    ]
    result = []
    for url in symbol_urls:
        symbols = getSymbolsFromGit(url)
        result += symbols
    return result

def getSymbolsFromGit(url):
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        symbols = decoded_content.splitlines()
    symbols = [item.strip() for item in symbols]
    symbols = list(filter(lambda x: x[0:1]!='^', symbols))
    return symbols

def saveQuotes():
    # get all symbols
    symbols = getAllSymbols()
    print(symbols, len(symbols))
    
    slice = 'year1month6'
    for index, symbol in enumerate(symbols):
        if index>0 and index % 5 ==0:
            print("sleep 60 seconds")
            time.sleep(62)
        print(f"download {symbol}")
        downloadQuotes(symbol, slice)

    # download forex  USD => EUR, USD => CNY
    time.sleep(62)
    downloadForex('USD', 'CNY', slice)
    downloadForex('USD', 'EUR', slice)
        

if __name__ == "__main__":
    saveQuotes()
    # symbols = getSymbolsFromGit('https://raw.githubusercontent.com/hairinwind/pyahoo/master/config/symbol.1.txt')
    # print(symbols)
    # downloadQuotes("CL=F", 'year1month1')
    