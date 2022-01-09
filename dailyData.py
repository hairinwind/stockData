import os
import pandas as pd
import shutil

dataPath = 'data/5min'
dailyPath = 'data/daily'

# marketOpen 09:35
# marketClose 16:00
"""
get the 16:00 close as the daily close
get the 09:40 open as the daily open
get the max of high as daily high
get the min of low as daily low 
"""
def fiveMinToDailyData():
    dataFile = os.path.join(dataPath, 'data.csv')
    data = pd.read_csv(dataFile)
    data = data[(data['hourTime'] >= '09:35:00') & (data['hourTime'] <= '16:05:00')]
    data = data.sort_values(by=['symbol', 'time'])
    df = data.groupby(['symbol', 'date']).agg({'symbol':'first', 'date': 'first', 'open':{'open':'first', 'close':'last'}, 
        'high':'max', 'low':'min', 'volume':'sum'})
    # rename columns
    df.columns = ['symbol', 'date', 'open', 'close', 'high', 'low', 'volume']
    
    # move column close after column low
    column_close = df.pop('close')
    df.insert(5, 'close', column_close)

    df = df.round(2)
    df.to_csv(os.path.join(dailyPath, 'daily_data.csv'), index=False)
    
if __name__ == "__main__":
    fiveMinToDailyData()