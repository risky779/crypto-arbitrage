#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY'), 'enableRateLimit': True})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE'), 'enableRateLimit': True})

print("=== 다중 코인 포지션 구축 ===\n", flush=True)

coins = ['ID', 'BAT', 'ALGO', 'MMT']

for coin in coins:
    try:
        # OKX에서 매수
        print(f"{coin}: OKX $5 매수...", flush=True)
        okx.create_market_buy_order(f'{coin}/USDT', 5)
        time.sleep(1)

        # 업비트에서 매수
        print(f"{coin}: 업비트 7,000원 매수...", flush=True)
        upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': 7000})
        time.sleep(1)

        print(f"{coin} 완료\n", flush=True)

    except Exception as e:
        print(f"{coin} 실패: {e}\n", flush=True)
        continue

print("포지션 구축 완료", flush=True)
