from binance.client import Client
import pandas as pd
import ta


def check_sar_signal(api_key, api_secret, symbol='BTCUSDT', start_str='1 Jan, 2022', end_str='1 Apr, 2022'):
    # Инициализация клиента Binance
    client = Client(api_key, api_secret)

    # Получаем исторические данные о ценах
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_str, end_str)

    # Создание DataFrame из полученных данных
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                       'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                       'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Рассчитываем Параболическую систему SAR
    df['sar'] = ta.trend.psar(df['high'], df['low'], df['close'], step=0.02, max_step=0.2)

    # Анализ последних двух точек для определения сигнала
    last_close = df.iloc[-1]['close']
    last_sar = df.iloc[-1]['sar']
    prev_sar = df.iloc[-2]['sar']

    # Сигнал к покупке: если SAR перешел ниже цены закрытия
    if last_sar < last_close and prev_sar > df.iloc[-2]['close']:
        return 1  # Сигнал к покупке
    # Сигнал к продаже: если SAR перешел выше цены закрытия
    elif last_sar > last_close and prev_sar < df.iloc[-2]['close']:
        return 0  # Сигнал к продаже
    else:
        return -1  # Нет четкого сигнала


# Замените 'your_api_key' и 'your_api_secret' на ваши ключи API с Binance
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Вызов функции
signal = check_sar_signal(api_key, api_secret)

# Вывод сигнала
print(signal)
