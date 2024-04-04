import numpy as np
import time
from datetime import datetime
from binance.client import Client


# exchange operations:
def short_open(symbol, quantity):
    client.futures_create_order(symbol=symbol,
                                side='SELL',
                                type='MARKET',
                                quantity=quantity)


def short_close(symbol, quantity):
    client.futures_create_order(symbol=symbol,
                                side='BUY',
                                type='MARKET',
                                quantity=quantity)


def long_open(symbol, quantity):
    client.futures_create_order(symbol=symbol,
                                side='BUY',
                                type='MARKET',
                                quantity=quantity)


def long_close(symbol, quantity):
    client.futures_create_order(symbol=symbol,
                                side='SELL',
                                type='MARKET',
                                quantity=quantity)


# initialize Client with your API keys
api_key = ""
api_secret = ""
client = Client(api_key, api_secret)

# traded symbol
symbol = "ETHUSDT"

# list to keep all closing prices
prices = []

# lists to keep all stats needed
moving_average_values = []
bollinger_band_high_values = []
bollinger_band_low_values = []

# flags to track the exchanges to avoid duplicated entries
in_short = False
in_long = False

# period of Bollinger bands
period = 3

last_time = ""


# main loop
def signal_handler():
    while True:
        current_time = datetime.now()
        # if current candlestick has closed and current time is not equal to the
        # latest record (to avoid duplicated price records)
        if current_time.minute % 5 == 0 and current_time.strftime('%Y-%m-%d %H:%M') != last_time:
            last_time = current_time.strftime('%Y-%m-%d %H:%M')
            # get latest price for the symbol
            latest_price = client.futures_symbol_ticker(symbol=symbol)['price']
            latest_price = float(latest_price)
            prices.append(latest_price)

            # print latest price with current time
            print(current_time, latest_price)

            # calculate moving average and deviation
            ma = np.mean(prices[-period:])
            moving_average_values.append(ma)

            std = np.std(prices[-period:], ddof=1)

            # calculate Bollinger bands
            bb_high = ma + 2 * std
            bb_low = ma - 2 * std

            bollinger_band_high_values.append(bb_high)
            bollinger_band_low_values.append(bb_low)

            # descion of the strategy
            # short exchanges
            if prices[-2] < bollinger_band_high_values[-2] and prices[-1] > bollinger_band_high_values[-1]:
                if not in_short:
                    short_open(symbol=symbol, quantity=1)
                    # return 0
                    in_short = True

            if prices[-2] > moving_average_values[-2] and prices[-1] < moving_average_values[-1]:
                if in_short:
                    short_close(symbol=symbol, quantity=1)
                    # return 1
                    in_short = False

            # long conditions
            if prices[-1] < bollinger_band_low_values[-1] and prices[-2] > bollinger_band_low_values[-2]:
                if not in_long:
                    long_open(symbol=symbol, quantity=1)
                    # return 1
                    in_long = True

            if prices[-2] < moving_average_values[-2] and prices[-1] > moving_average_values[-1]:
                if in_long:
                    long_close(symbol=symbol, quantity=1)
                    # return 0
                    in_long = False


if __name__ == '__main__':
    signal_handler()
