from binance.client import Client
import pandas as pd
import ta


def get_dmi_signals(api_key, api_secret, symbol='BTCUSDT', start_str='1 Jan, 2022', end_str='1 Apr, 2022'):
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

    # Рассчитываем DMI и ADX
    df['adx'] = ta.trend.adx(df['high'], df['low'], df['close'])
    df['plus_di'] = ta.trend.adx_pos(df['high'], df['low'], df['close'])
    df['minus_di'] = ta.trend.adx_neg(df['high'], df['low'], df['close'])

    # Инициализация колонки сигналов
    df['signal'] = -1  # Инициализация колонки сигналов значением для 'нет сигнала'

    # Проверка на сигналы
    for i in range(1, len(df)):
        if df.iloc[i]['plus_di'] > df.iloc[i]['minus_di'] and df.iloc[i]['adx'] > 25 and df.iloc[i - 1]['plus_di'] <= \
                df.iloc[i - 1]['minus_di']:
            df.at[df.index[i], 'signal'] = 1  # Сигнал к покупке
        elif df.iloc[i]['minus_di'] > df.iloc[i]['plus_di'] and df.iloc[i]['adx'] > 25 and df.iloc[i - 1]['minus_di'] <= \
                df.iloc[i - 1]['plus_di']:
            df.at[df.index[i], 'signal'] = 0  # Сигнал к продаже

    # Возвращает DataFrame с добавленными сигналами
    return df


# Замените 'your_api_key' и 'your_api_secret' на ваши ключи API с Binance
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Вызов функции
df_signals = get_dmi_signals(api_key, api_secret)

# Вывод последних строк DataFrame для просмотра
print(df_signals[['plus_di', 'minus_di', 'adx', 'signal']].tail())
