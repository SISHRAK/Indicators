from binance.client import Client
import pandas as pd

# Замените на ваши ключи API
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Создание клиента Binance
client = Client(api_key, api_secret)


def get_historical_data(symbol, interval, start_str, end_str=None):
    """
    Получение исторических данных о ценах и объемах.
    """
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
               'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
               'taker_buy_quote_asset_volume', 'ignore']

    bars = client.get_historical_klines(symbol, interval, start_str, end_str)
    df = pd.DataFrame(bars, columns=columns)
    df['close'] = pd.to_numeric(df['close'])
    df['volume'] = pd.to_numeric(df['volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df[['timestamp', 'close', 'volume']]

# need to 1 or 0
def calculate_obv(df):
    """
    Расчет On-Balance Volume (OBV).
    """
    df['daily_return'] = df['close'].diff()
    df['direction'] = df['daily_return'].apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)
    df['adjusted_volume'] = df['direction'] * df['volume']
    df['OBV'] = df['adjusted_volume'].cumsum()
    return df


#TODO

