from binance.client import Client
import pandas as pd
import ta
from binance.exceptions import BinanceAPIException
import time

api_key = ''
secret = ''

client = Client(api_key=api_key, api_secret=secret)


def klines(symbol):
    try:
        df = pd.DataFrame(client.get_historical_klines(symbol, '1m', '40m UTC'))
    except BinanceAPIException as e:
        print(e)
        time.sleep(60)
        df = pd.DataFrame(client.get_historical_klines(symbol, '1m', '40m UTC'))

    df = df.iloc[:, :6]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df.set_index('Time')
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.astype(float)
    return df


def strategy(symbol, qty, open_position):
    while True:
        df = klines(symbol)
        if not open_position:
            if ta.trend.macd_diff(df.Close).iloc[-1] > 0 > ta.trend.macd_diff(df.Close).iloc[-2]:
                return 1
        if open_position:
            df = klines(symbol)
            if ta.trend.macd_diff(df.Close).iloc[-1] < 0 < ta.trend.macd_diff(df.Close).iloc[-2]:
                return 0


strategy('ALGOUSDT', qty=33, open_position=True)
