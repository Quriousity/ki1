# OHLCV 다듬기
from market import GetOHLCV
# Binance Futures API
from binance.um_futures import UMFutures
# Binance Client
client = UMFutures()

# 종목
ticker = '1000RATSUSDT'
# 시작 (YYYY-mm-dd)
start = '2024-06-13 18:00:00'
# 끝 (YYYY-mm-dd)
end = '2024-06-13 20:00:00'
# 간격 (1m, 1h, 4h, 1d, ...)
interval = '1h'

# OHLCV
df = GetOHLCV(client, ticker, interval, start, end)
print(df)