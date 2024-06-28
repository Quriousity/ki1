# 스케줄
import schedule
# HTTP request
import requests
# 시간 모듈1
from time import sleep
# 시간 모듈2
from datetime import datetime
# OHLCV 다듬기
from market import GetOHLCVRecent, datetimeToStr
# Binance Futures API
from binance.um_futures import UMFutures
# Binance Client
client = UMFutures()


ei = client.exchange_info()
# 티커 이름 모음
tickers = []
# 거래소 정보중에
for i in ei['symbols']:
    # 이름에 USDT가 들어가고
    if 'USDT' in i['symbol']:
        # 상태가 TRADING 인
        if i['status']=='TRADING':
            # 녀석들
            tickers.append(i['symbol'])

ticker = 'FRONTUSDT'
print(ticker)
# 최근 캔들 100개
df = GetOHLCVRecent(client, ticker, '1h', 1000)
# 5일선
df['ma5'] = df['close'].ewm(span=5).mean()
# 25일선
df['ma25'] = df['close'].ewm(span=25).mean()
print(df)
print(df['ma5'].iloc[-2], df['ma25'].iloc[-2])
print(df['ma5'].iloc[-1], df['ma25'].iloc[-1])
'''

# Golden Cross
if df['ma5'].iloc[-1] > df['ma25'].iloc[-1]:
    if df['ma5'].iloc[-2] < df['ma25'].iloc[-2]:
        # 현재 시간
        t = datetimeToStr(datetime.now())
        message = '{}({}) {} {}'.format(ticker, interval, t, 'Golden Cross')
        print(message)
        SendTelegram(message)
# Dead Cross
if df['ma5'].iloc[-1] < df['ma25'].iloc[-1]:
    if df['ma5'].iloc[-2] > df['ma25'].iloc[-2]:
        # 현재 시간
        t = datetimeToStr(datetime.now())
        message = '{}({}) {} {}'.format(ticker, interval, t, 'Dead Cross')
        print(message)
        SendTelegram(message)
'''
