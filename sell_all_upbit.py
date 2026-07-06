#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY'), 'enableRateLimit': True})

print("=== 업비트 전체 매도 ===\n", flush=True)

bal = upbit.fetch_balance()

for coin in ['BAT', 'MMT', 'ALGO', 'BCH', 'ID', 'XRP', 'XLM']:
    free = bal.get(coin, {}).get('free', 0)
    if free > 0.0001:
        try:
            ticker = upbit.fetch_ticker(f'{coin}/KRW')
            value = free * ticker['last']

            if value < 5000:
                print(f"{coin}: {free:.6f}개 ({value:.0f}원) - 최소금액 미만\n", flush=True)
                continue

            print(f"{coin}: {free:.6f}개 ({value:.0f}원) 매도 중...", flush=True)
            order = upbit.create_market_sell_order(f'{coin}/KRW', free)
            print(f"✅ {order['cost']:,.0f}원 확보\n", flush=True)
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ {coin} 매도 실패: {e}\n", flush=True)

bal = upbit.fetch_balance()
print(f"업비트 최종 KRW: {bal['KRW']['free']:,.0f}원", flush=True)
