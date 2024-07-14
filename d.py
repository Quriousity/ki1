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

# Telegram 알림
def SendTelegram(message):
    token = "6547837409:AAFe5KZSUDfEs0ZLN4oInDS4bP-wizgO3XE"
    chat_id = "1586291617"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + message 
    requests.get(url_req)


def CheckAD(df):
    # 5일선 (EMA)
    df['ma5'] = df['close'].ewm(span=5).mean()
    # 25일선 (EMA)
    df['ma25'] = df['close'].ewm(span=25).mean()
    # 60일선 (EMA)
    df['ma60'] = df['close'].ewm(span=60).mean()
    # 200일선 (EMA)
    df['ma200'] = df['close'].ewm(span=200).mean()

    ma5, ma25, ma60, ma200 = df['ma5'].iloc[-1], df['ma25'].iloc[-1], df['ma60'].iloc[-1], df['ma200'].iloc[-1]
    if ma5 > ma25 and ma25 > ma60 and ma60 > ma200:
        return '정배열'
    if ma5 < ma25 and ma25 < ma60 and ma60 < ma200:
        return '역배열'


# 현재 시간
def Alert(ticker, interval):
    t = datetimeToStr(datetime.now())
    message = '{} {} {}({})'.format(ticker, t, '정배열', interval)
    print(message)


# Ascending/Decending
def AD():
    # 티커 정보
    ei = client.exchange_info()
    # 티커 이름 리스트
    tickers = []
    # 거래소 정보중에
    for i in ei['symbols']:
        # 이름에 USDT가 들어가고
        if 'USDT' in i['symbol']:
            # 상태가 TRADING 인
            if i['status']=='TRADING':
                # 녀석들
                tickers.append(i['symbol'])
    # 티커 순회
    for ticker in tickers:
        sleep(0.1)
        # 최근 캔들 1000개
        # df = GetOHLCVRecent(client, ticker, '1w', 1000); sleep(0.1)
        # if CheckAD(df) == '정배열':
        df = GetOHLCVRecent(client, ticker, '1d', 1000); sleep(0.1)
        if CheckAD(df) == '정배열':
            df = GetOHLCVRecent(client, ticker, '4h', 1000); sleep(0.1)
            if CheckAD(df) == '정배열':
                df = GetOHLCVRecent(client, ticker, '1h', 1000); sleep(0.1)
                if CheckAD(df) == '정배열':
                    df = GetOHLCVRecent(client, ticker, '30m', 1000); sleep(0.1)
                    if CheckAD(df) == '정배열':
                        df = GetOHLCVRecent(client, ticker, '15m', 1000); sleep(0.1)
                        if CheckAD(df) == '정배열':
                            df = GetOHLCVRecent(client, ticker, '5m', 1000); sleep(0.1)
                            if CheckAD(df) == '정배열':
                                df = GetOHLCVRecent(client, ticker, '1m', 1000); sleep(0.1)
                                if CheckAD(df) == '정배열':
                                    # 현재 시간
                                    t = datetimeToStr(datetime.now())
                                    message = '{} {} {}'.format(ticker, t, '정배열')
                                    print(message)
                                    SendTelegram(message)

        # df = GetOHLCVRecent(client, ticker, '1w', 1000); sleep(0.1)
        # if CheckAD(df) == '역배열':
        df = GetOHLCVRecent(client, ticker, '1d', 1000); sleep(0.1)
        if CheckAD(df) == '역배열':
            df = GetOHLCVRecent(client, ticker, '4h', 1000); sleep(0.1)
            if CheckAD(df) == '역배열':
                df = GetOHLCVRecent(client, ticker, '1h', 1000); sleep(0.1)
                if CheckAD(df) == '역배열':
                    df = GetOHLCVRecent(client, ticker, '30m', 1000); sleep(0.1)
                    if CheckAD(df) == '역배열':
                        df = GetOHLCVRecent(client, ticker, '15m', 1000); sleep(0.1)
                        if CheckAD(df) == '역배열':
                            df = GetOHLCVRecent(client, ticker, '5m', 1000); sleep(0.1)
                            if CheckAD(df) == '역배열':
                                df = GetOHLCVRecent(client, ticker, '1m', 1000); sleep(0.1)
                                if CheckAD(df) == '역배열':
                                    # 현재 시간
                                    t = datetimeToStr(datetime.now())
                                    message = '{} {} {}'.format(ticker, t, '역배열')
                                    print(message)
                                    SendTelegram(message)

# 스케줄 등록
# 매주 월요일 9시 10초
schedule.every().monday.at('09:00:10').do(AD)

while True:
    schedule.run_pending()
    sleep(1)
