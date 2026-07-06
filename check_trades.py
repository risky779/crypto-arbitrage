#!/usr/bin/env python3
import ccxt, os, sys, io
from datetime import datetime, timedelta
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({
    'apiKey': os.getenv('UPBIT_ACCESS_KEY'),
    'secret': os.getenv('UPBIT_SECRET_KEY'),
})

print("=== 최근 거래 내역 ===\n")

# 최근 거래 조회
try:
    # 여러 마켓 조회
    markets = ['BAT/KRW', 'MMT/KRW', 'ID/KRW', 'ALGO/KRW', 'BCH/KRW']

    all_trades = []

    for market in markets:
        try:
            trades = upbit.fetch_my_trades(market, limit=20)
            all_trades.extend(trades)
        except:
            continue

    # 시간순 정렬
    all_trades.sort(key=lambda x: x['timestamp'], reverse=True)

    total_profit = 0

    for trade in all_trades[:30]:
        dt = datetime.fromtimestamp(trade['timestamp'] / 1000)
        symbol = trade['symbol']
        side = trade['side']
        amount = trade['amount']
        price = trade['price']
        cost = trade['cost']

        sign = '-' if side == 'buy' else '+'

        print(f"{dt.strftime('%m-%d %H:%M')} | {symbol} | {side:4s} | {amount:.6f} | {cost:,.0f}원", flush=True)

        if side == 'sell':
            total_profit += cost
        else:
            total_profit -= cost

    print(f"\n순손익 추정: {total_profit:,.0f}원")

except Exception as e:
    print(f"오류: {e}")
