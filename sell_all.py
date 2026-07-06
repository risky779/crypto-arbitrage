#!/usr/bin/env python3
import ccxt, os, sys, io
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY'), 'enableRateLimit': True})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE'), 'enableRateLimit': True})

print("=== OKX 전액 매각 ===\n", flush=True)

# OKX 보유자산 매각
okx_bal = okx.fetch_balance()
for coin in ['BCH', 'USDT', 'XRP', 'XLM', 'ALGO', 'ID', 'MMT', 'BAT']:
    if coin == 'USDT':
        continue

    free = okx_bal.get(coin, {}).get('free', 0)
    if free > 0:
        try:
            print(f"OKX {coin} {free:.8f}개 매도", flush=True)
            order = okx.create_market_sell_order(f'{coin}/USDT', free * 0.99)
            print(f"✅ ${order['cost']:.2f} USDT 확보", flush=True)
        except Exception as e:
            print(f"❌ {coin} 매도 실패: {e}", flush=True)

okx_bal = okx.fetch_balance()
print(f"\nOKX 최종: ${okx_bal['USDT']['free']:.2f} USDT\n", flush=True)

print("=== 업비트 전액 매각 ===\n", flush=True)

# 업비트 보유자산 매각
upbit_bal = upbit.fetch_balance()
for coin in ['BAT', 'MMT', 'BCH', 'ALGO', 'ID', 'XRP', 'XLM']:
    free = upbit_bal.get(coin, {}).get('free', 0)
    if free > 0:
        try:
            print(f"업비트 {coin} {free:.6f}개 매도", flush=True)
            order = upbit.create_market_sell_order(f'{coin}/KRW', free)
            print(f"✅ {order['cost']:,.0f}원 확보", flush=True)
        except Exception as e:
            print(f"❌ {coin} 매도 실패: {e}", flush=True)

upbit_bal = upbit.fetch_balance()
print(f"\n업비트 최종: {upbit_bal['KRW']['free']:,.0f}원", flush=True)
