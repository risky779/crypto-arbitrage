#!/usr/bin/env python3
import ccxt, os, sys, io
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE'), 'enableRateLimit': True})

print("OKX ID 매도 중...\n", flush=True)

bal = okx.fetch_balance()
id_qty = bal['ID']['free']

if id_qty > 0.1:
    try:
        ticker = okx.fetch_ticker('ID/USDT')
        value = id_qty * ticker['last']
        print(f"ID {id_qty:.2f}개 (${value:.2f})", flush=True)

        sell = okx.create_market_sell_order('ID/USDT', id_qty)
        print(f"✅ ${sell['cost']:.2f} USDT 확보", flush=True)
    except Exception as e:
        print(f"❌ 매도 실패: {e}", flush=True)

bal = okx.fetch_balance()
print(f"\nOKX 최종 USDT: ${bal['USDT']['free']:.2f}", flush=True)
