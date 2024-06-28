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

# 간격 (1m, 1h, 4h, 1d, ...)
interval = input('간격 (1m, 1h, 4h, 1d, ...): ')

# 거래가 가능한 티커 모음
tickers = []

# Telegram 알림
def SendTelegram(message):
    token = "6547837409:AAFe5KZSUDfEs0ZLN4oInDS4bP-wizgO3XE"
    chat_id = "1586291617"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + message 
    requests.get(url_req)

def RefreshTickers():
    global tickers
    # 거래소 정보
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

# Golden/Dead Cross
def GD():
    global tickers, interval
    # 티커 순회
    for ticker in tickers:
        sleep(0.2)
        # 최근 캔들 100개
        df = GetOHLCVRecent(client, ticker, interval, 1000)
        # 5일선
        df['ma5'] = df['close'].ewm(span=5).mean()
        # 25일선
        df['ma25'] = df['close'].ewm(span=25).mean()
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


# Initialize
RefreshTickers()
GD()

# 스케줄 등록
# 매일 10시에 티커정보 업데이트
schedule.every().day.at("10:00:00").do(RefreshTickers)
# 봉간격 1시간이면
if interval == "1h":
    time = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
    for i in time:
        schedule.every().day.at("{}:00:10".format(i)).do(GD)
# 봉간격 4시간이면
if interval == "4h":
    time = ['09', '13', '17', '21', '01', '05']
    for i in time:
        schedule.every().day.at("{}:00:10".format(i)).do(GD)
# 봉간격 하루면
if interval == "1d":
    schedule.every().day.at("09:00:10").do(GD)

while True:
    schedule.run_pending()
    sleep(1)