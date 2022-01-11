from globalSettings import fiveMinuteFile, dailyFile, hourlyFile
import pandas as pd

hours=[
    '09:35:00',
    '10:00:00',
    '11:00:00',
    '12:00:00',
    '13:00:00',
    '14:00:00',
    '15:00:00',
    '16:00:00',
    '16:05:00'
]

def getAllSymbols(data):
    symbol_set = data.drop_duplicates(subset=['symbol'])['symbol'].tolist()
    return symbol_set

def check(data, check_time):
    symbol_set = getAllSymbols(data)
    day1 = data[data['time'] == check_time]
    symbols_day1 = day1.drop_duplicates(subset=['symbol'])['symbol'].tolist()
    # print(len(symbols_day1))
    notFound = [x for x in symbol_set if x not in symbols_day1]
    return notFound

"""
generate hourlyData from 5 minute and daily data (custom indicators)
"""
def hourlyData():
    # get data from 2021-11-05 to 2021-11-17
    fiveMinuteData = pd.read_csv(fiveMinuteFile)
    # fiveMinuteData = fiveMinuteData[(fiveMinuteData['date'] >= '2021-11-05') & (fiveMinuteData['date'] <= '2021-11-17')]
    fiveMinuteData = fiveMinuteData.query('hourTime in @hours')
    print(fiveMinuteData)

    dailyData = pd.read_csv(dailyFile)
    dailyData = dailyData[['symbol', 'date', 'SMA10', 'SMA20', 'RSI', 'OBV', 'ADL', 'STOCH']]

    df = pd.merge(fiveMinuteData, dailyData, on=['symbol', 'date'])
    # print(f"ARKQ after merge")
    # print(df[(df.symbol=='ARKQ') & (df.date=='2021-10-11')])
    df = df.round(3)

    # TODO, drop currency for now
    df = df.drop(df[(df.symbol == 'USDCNY') | (df.symbol == 'USDEUR')].index)
    df.sort_values(by=['time','symbol'], inplace=True)
    df = df.drop_duplicates(subset=['time', 'symbol'])

    # amend missed quotes
    date_set = df.drop_duplicates(subset=['date'])['date'].tolist()
    for date in date_set:
        for hour in hours:
            time = f"{date} {hour}"
            print(f"check {time}")
            missedQuotes = check(df, time)
            for symbol in missedQuotes:
                df.sort_values(by=['time','symbol'], inplace=True)
                df1 = df[(df['symbol'] == symbol)& (df['time']<time)].tail(1).copy()
                df1['time'] = time
                df1['date'] = df1['time'].apply(lambda x: x[0:10])
                df1['hourTime'] = df1['time'].apply(lambda x: x[11:20])
                if symbol == 'AAPL' and time=='2021-11-26 14:00':
                    print(f"amend {symbol} {time} with {df1}")
                df = df.append(df1)
        missedQuotes = check(df, time)
        assert len(missedQuotes) == 0

    df1 = df.groupby(['time'])['symbol'].describe()[['count']]
    df2 = df1[df1['count']!=120]
    print(df2)
    assert len(df2) == 0

    df.to_csv(hourlyFile, index=False)

def verify():
    df = pd.read_csv(hourlyFile)
    # count by time
    df1 = df.groupby(['time'])['symbol'].describe()[['count']]
    df2 = df1[df1['count']!=120]
    assert len(df2) == 0

    # count by day
    df3 = df.groupby(['date','symbol'])['hourTime'].describe()[['count']]
    df4 = df3[df3['count'] != 9]
    assert len(df4) == 0

    print(len(df))
    print(f"{len(df)}/9/120={len(df)/9.0/120.0}")
    # df3 = df[(df.symbol=='AAPL') & (df.date=='2021-11-26')]
    # print(df3)

    
if __name__ == "__main__":
    # hourlyData()
    verify()