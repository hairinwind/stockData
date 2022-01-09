from finta import TA
import os
import pandas as pd

dailyPath = 'data/daily'

def addIndicators():
    file = os.path.join(dailyPath, 'daily_data.csv')
    df = pd.read_csv(file)

    df.reset_index(drop=True, inplace=True)
    df['SMA10'] = TA.SMA(df, 10)
    df['SMA20'] = TA.SMA(df, 20)
    df['RSI'] = TA.RSI(df)
    df['OBV'] = TA.OBV(df)
    df['ADL'] = TA.ADL(df)
    # df['MACD'] = TA.VW_MACD(df)
    # df['BBANDS'] = TA.BBANDS(df)
    df['STOCH'] = TA.STOCH(df)
    df.fillna(0, inplace=True)
    df = df.round(3)
    df.to_csv(file, index=False)


if __name__ == "__main__":
    addIndicators()