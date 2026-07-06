#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY'), 'enableRateLimit': True})

print("=== 업비트 보유자산 매도 ===\n", flush=True)

upbit_bal = upbit.fetch_balance()

for coin in ['BAT', 'MMT']:
    free = upbit_bal.get(coin, {}).get('free', 0)
    if free > 0:
        try:
            ticker = upbit.fetch_ticker(f'{coin}/KRW')
            value = free * ticker['last']
            print(f"업비트 {coin}: {free:.6f}개 ({value:,.0f}원)", flush=True)

            if value >= 5000:
                order = upbit.create_market_sell_order(f'{coin}/KRW', free)
                print(f"✅ {order['cost']:,.0f}원 확보\n", flush=True)
                time.sleep(0.5)
            else:
                print(f"❌ 5000원 미만 거래 불가\n", flush=True)
        except Exception as e:
            print(f"❌ {coin} 매도 실패: {e}\n", flush=True)

upbit_bal = upbit.fetch_balance()
print(f"업비트 최종 KRW: {upbit_bal['KRW']['free']:,.0f}원", flush=True)
