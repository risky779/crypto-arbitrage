#!/usr/bin/env python3
import ccxt
import os
from dotenv import load_dotenv

load_dotenv()

upbit = ccxt.upbit({
    'apiKey': os.getenv('UPBIT_ACCESS_KEY'),
    'secret': os.getenv('UPBIT_SECRET_KEY'),
})

print("업비트 전량 매도 시작\n")

balance = upbit.fetch_balance()

# 보유 코인 찾기
for symbol in balance:
    if symbol in ['free', 'used', 'total', 'KRW', 'info', 'timestamp', 'datetime']:
        continue

    amount = balance[symbol].get('free', 0)
    if amount > 0.0001:
        print(f"{symbol}: {amount:.8f} 매도 중...", end=' ')
        try:
            order = upbit.create_market_sell_order(f'{symbol}/KRW', amount * 0.99)
            print(f"완료!")
        except Exception as e:
            print(f"실패: {e}")

print("\n매도 완료")
