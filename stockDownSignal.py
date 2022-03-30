""" 
这个是在历史数据中查找股票下跌的一些信号
比如：找连续三天下跌的第一天下跌百分比中位数
"""

import os
import pandas as pd

def readCsv(symbol, rows):
    filename = "daily_"+symbol.upper()+".csv"
    file = os.path.join('data/daily', filename)
    csv = pd.read_csv(file, nrows=rows)
    return csv

def medianFirstDayFor3DaysDown(symbol, period) :
    """
    get the median percentage of the first day of 3 continues down 
    Parameters
    ----------
    symbol : str
        The sound the animal makes (default is None)
    period：number 
        this is the number of months, e.g. 12 means in past 12 months, 3 menas in past 3 months
    """
    data = readCsv(symbol, period * 31) # no need to be 100% accurate 
    print(len(data))
    data['change'] = data.close - data.close.shift(-1)
    data['firstOf3Down'] = data.change < 0 and data.change.shift(-1) < 0 and data.change.shift(-2) < 0
    print(data.head(5))


if __name__ == "__main__":
    medianFirstDayFor3DaysDown("TECL", 12)
