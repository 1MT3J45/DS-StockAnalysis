"""
Retrieve intraday stock data from Google Finance.
"""

import csv
import datetime
import re
import pandas as pd

import requests


def get_google_finance_intraday(ticker, period, days):
    """
    Retrieve intraday stock data from Google Finance.
    Parameters
    ----------
    ticker : str
        Company ticker symbol.
    period : int
        Interval between stock values in seconds.
    days : int
        Number of days of data to retrieve.
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """

    uri = 'http://www.google.com/finance/getprices' \
          '?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'.format(ticker=ticker,
                                                                          period=period,
                                                                          days=days)
    page = requests.get(uri)
    reader = csv.reader(page.content.splitlines())
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    rows = []
    times = []
    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start + datetime.timedelta(seconds=period * int(row[0])))
            rows.append(map(float, row[1:]))
    if len(rows):
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),
                            columns=columns)

    else:
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))


def write_csv(self, filename):
    with open(filename, 'w') as f:
        f.write(self.to_csv())

TCKR = pd.read_csv('TICKERS_testing.csv')
df_list = list()
df_avg_list = list()
for i in range(TCKR.__len__()):
    print("%s".center(40, '_')%TCKR.iloc[i, 0])
    df_list.append(get_google_finance_intraday(TCKR.iloc[i,0], 3600, 1))
    if not df_list[i].empty:
        dim = df_list[i].shape
        df_list[i]['Ticker'] = pd.Series([TCKR.iloc[i, 0]]*dim[0]).values.reshape(-1, 1)
        print(df_list[i])
    else:
        print 'No Stocks recorded for', TCKR.iloc[i,0]
# TODO Get avg of OHLC & Store in CSV
StockConclave = pd.concat(df_list)
df = StockConclave.values
StockConclave.to_csv('Results/StockConclave.csv')
