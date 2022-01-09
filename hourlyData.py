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
    df = df.round(3)
    df.to_csv(hourlyFile, index=False)

    
if __name__ == "__main__":
    hourlyData()