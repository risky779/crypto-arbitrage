#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE'), 'enableRateLimit': True})

print("=== OKX 코인 전액 매도 ===\n", flush=True)

okx_bal = okx.fetch_balance()

for coin in ['ALGO', 'ID', 'BCH']:
    free = okx_bal.get(coin, {}).get('free', 0)
    if free > 0.0001:
        try:
            ticker = okx.fetch_ticker(f'{coin}/USDT')
            print(f"OKX {coin}: {free:.6f}개 (${free * ticker['last']:.2f})", flush=True)

            order = okx.create_market_sell_order(f'{coin}/USDT', free)
            print(f"✅ ${order['cost']:.2f} USDT 확보\n", flush=True)
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ {coin} 매도 실패: {e}\n", flush=True)

okx_bal = okx.fetch_balance()
print(f"OKX 최종 USDT: ${okx_bal['USDT']['free']:.2f}", flush=True)
