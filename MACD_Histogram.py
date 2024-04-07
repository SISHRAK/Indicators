from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt


api_key = 'your_api_key'
api_secret = 'your_api_secret'

client = Client(api_key, api_secret, testnet=True)

def get_historical_prices(symbol, interval, start_str, end_str=None):
    bars = client.get_historical_klines(symbol, interval, start_str, end_str)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    df['close'] = pd.to_numeric(df['close'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[['timestamp', 'close']]

def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    df['EMA_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['EMA_long'] = df['close'].ewm(span=long_period, adjust=False).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal_line'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    df['MACD_histogram'] = df['MACD'] - df['Signal_line']
    return df

# Пример использования
symbol = 'BTCUSDT'
interval = '1d'
start_str = '1 Jan, 2020'

df = get_historical_prices(symbol, interval, start_str)
macd_df = calculate_macd(df)

# Визуализация MACD и его гистограммы
plt.figure(figsize=(14, 7))
plt.plot(macd_df['timestamp'], macd_df['MACD'], label='MACD')
plt.plot(macd_df['timestamp'], macd_df['Signal_line'], label='Signal line')
plt.bar(macd_df['timestamp'], macd_df['MACD_histogram'], label='MACD Histogram', color='gray')
plt.legend()
plt.show()
