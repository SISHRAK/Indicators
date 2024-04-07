import pandas as pd
import numpy as np
from binance.client import Client
api_key = ""
api_secret = ""

client = Client(api_key, api_secret)
def get_historical_prices(symbol, interval, start_str, end_str=None):
    bars = client.get_historical_klines(symbol, interval, start_str, end_str)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    df['close'] = pd.to_numeric(df['close'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Функция для расчета скользящего среднего
def calculate_sma(data, window):
    return data['close'].rolling(window=window).mean()


def moving_average_strategy(data, short_window, long_window):
    # Расчет скользящих средних
    data['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1).mean()
    data['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1).mean()

    # Поиск точек пересечения
    data['signal'] = 0  # Стандартное значение - отсутствие действия
    data['signal'][short_window:] = np.where(data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1, 0)
    data['positions'] = data['signal'].diff()

    if data['positions'].iloc[-1] > 0:
        return 1  # Покупка
    elif data['positions'].iloc[-1] < 0:
        return 0  # Продажа
    else:
        return -1  # Отсутствие действия