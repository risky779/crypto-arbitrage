#!/usr/bin/env python3
import ccxt, os, sys, io
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY')})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})

print("=== 양방향 포지션 구축 ===\n", flush=True)

# OKX에서 ID 매수
print("OKX에서 ID $20 매수...", flush=True)
okx.create_market_buy_order('ID/USDT', 20)

# 업비트에서 ID 매수
print("업비트에서 ID 25,000원 매수...", flush=True)
upbit.create_order('ID/KRW', 'market', 'buy', None, None, {'cost': 25000})

print("\n완료. 양방향 거래 준비됨", flush=True)
