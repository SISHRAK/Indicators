from binance.client import Client


def get_vwap(symbol=None, interval=None, start_str=None, klines=None, interval_number=5):
    if not klines:
        if ((not symbol) and (not interval) and (not start_str)):
            print("Missing at least klines OR symbol,interval,start_str")
            raise ValueError("Missing at least klines OR symbol,interval,start_str")

        else:
            klines = klines(symbol, interval, start_str)

    # Initialization
    temp_typical_price_times_volume = 0.0
    temp_volume = 0.0
    # VWAP = ∑ (Typical Price * Volume ) / ∑ Volume
    for i in range(len(klines) - interval_number, len(klines)):
        high_price = float(klines[i][2])
        low_price = float(klines[i][3])
        close_price = float(klines[i][4])

        # Typical price
        typical_price = (high_price + low_price + close_price) / 3

        volume = float(klines[i][5])

        temp_typical_price_times_volume += typical_price * volume

        temp_volume += volume

    # VWAP = ∑ (Typical Price * Volume ) / ∑ Volume
    vmap = temp_typical_price_times_volume / temp_volume
    return vmap
