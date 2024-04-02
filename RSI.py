import pandas as pd
from binance.um_futures import UMFutures
import ta

API_KEY = ""
API_SECRET_KEY = ""

client = UMFutures(API_KEY, API_SECRET_KEY)


def get_data(symbol, interval):
    klines = client.klines(symbol, interval=interval, limit=100)
    return_data = []
    for each in klines:
        return_data.append(float(each[4]))
    return return_data


def get_rsi(symbol, interval):
    klines = client.klines(symbol, interval=interval, limit=7 + 1)
    closing_data = [float(each[4]) for each in klines]
    closing_series = pd.Series(closing_data)
    rsi = ta.momentum.RSIIndicator(closing_series, window=7).rsi()
    current_rsi = rsi.iloc[-1]  # Получение последнего значения RSI
    return current_rsi


def info():
    rsi = get_rsi()
    if rsi <= 20:
        return 0
    if rsi >= 80:
        return 1

if __name__ == "__main__":
    info()
    
