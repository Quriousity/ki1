# OHLCV 다듬기
from market import GetOHLCV
# Binance Futures API
from binance.um_futures import UMFutures
# Binance Client
client = UMFutures()

# 종목
ticker = input('종목 ex)BTCUSDT: ')
# 시작 (YYYY-mm-dd)
start = input('시작날짜(YYYY-mm-dd HH:MM:SS): ')
# 끝 (YYYY-mm-dd)
end = input('끝날짜(YYYY-mm-dd HH:MM:SS): ')
# 간격 (1m, 1h, 4h, 1d, ...)
interval = input('간격 (1m, 1h, 4h, 1d, ...): ')

# OHLCV
df = GetOHLCV(client, ticker, interval, start, end)
# 양 거래량
positive = 0
# 음 거래량
negative = 0
for open_, close_, volume in zip(df['open'], df['close'], df['volume']):
    if open_ < close_:
        positive += volume
    elif open_ > close_:
        negative += volume


print("+", format(int(positive), ','), "-", format(int(negative), ','), '=', format(int(positive-negative), ','))