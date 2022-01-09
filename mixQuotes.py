import os
import pandas as pd
import shutil

dataPath = 'data/5min'
quotePath = 'quotes'
quoteArchivePath = 'quotes/archive'

def mixQuotes():
    result = []
    for file in os.listdir(quotePath):
        filePath = os.path.join(quotePath, file)
        if os.path.isfile(filePath):
            symbol = file[:-16]
            quotes = pd.read_csv(filePath)
            quotes['symbol']=symbol
            quotes.rename(columns={'timestamp': 'time'}, inplace=True)
            result.append(quotes)
            # archive file
            shutil.move(filePath, os.path.join(quoteArchivePath, file))
    df = pd.concat(result)
    # add date and hourTime column
    df['date'] = df['time'].apply(lambda x: x[0:10])
    df['hourTime'] = df['time'].apply(lambda x: x[11:20])
    print(df)
    df.to_csv(os.path.join(dataPath, 'data.csv'), index=False)

if __name__ == "__main__":
    smixQuotes()
    # file = os.path.join(dataPath, 'data.csv')
    # df = pd.read_csv(file)
    # df['date'] = df['time'].apply(lambda x: x[0:10])
    # df['hourTime'] = df['time'].apply(lambda x: x[11:20])
    # df.to_csv(file, index=False)