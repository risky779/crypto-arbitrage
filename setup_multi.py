#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY'), 'enableRateLimit': True})

print("=== 업비트 다중 코인 포지션 ===\n", flush=True)

coins = ['ID', 'BAT', 'ALGO']

for coin in coins:
    try:
        print(f"{coin}: 8,000원 매수...", flush=True)
        upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': 8000})
        time.sleep(1)

        bal = upbit.fetch_balance()
        qty = bal.get(coin, {}).get('free', 0)
        print(f"  완료: {qty:.2f}개\n", flush=True)
    except Exception as e:
        print(f"  실패: {e}\n", flush=True)

bal = upbit.fetch_balance()
print(f"남은 KRW: {bal['KRW']['free']:,.0f}원", flush=True)
