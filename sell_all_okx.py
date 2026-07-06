#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE'), 'enableRateLimit': True})

print("=== OKX 전체 매도 ===\n", flush=True)

bal = okx.fetch_balance()

for coin in ['ID', 'ALGO', 'BCH', 'BAT', 'MMT', 'XRP', 'XLM']:
    free = bal.get(coin, {}).get('free', 0)
    if free > 0.01:
        try:
            ticker = okx.fetch_ticker(f'{coin}/USDT')
            value = free * ticker['last']
            print(f"{coin}: {free:.6f}개 (${value:.2f}) 매도 중...", flush=True)

            order = okx.create_market_sell_order(f'{coin}/USDT', free)
            print(f"✅ ${order['cost']:.2f} USDT 확보\n", flush=True)
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ {coin} 매도 실패: {e}\n", flush=True)

bal = okx.fetch_balance()
print(f"OKX 최종 USDT: ${bal['USDT']['free']:.2f}", flush=True)
