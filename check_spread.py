#!/usr/bin/env python3
import ccxt, os, sys, io
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY')})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})

RATE = 1480

print("=== 현재 차익률 ===\n", flush=True)

for coin in ['XRP','XLM','ALGO','BCH','ID','MMT','BAT']:
    try:
        o = okx.fetch_ticker(f'{coin}/USDT')
        u = upbit.fetch_ticker(f'{coin}/KRW')

        op = o['last']
        up = u['last']
        ok = op * RATE

        pn = ((up - ok) / ok) * 100 - 0.15
        pr = ((ok - up) / up) * 100 - 0.15

        arrow = "→" if pn > pr else "←"
        best = max(pn, pr)

        status = "✅" if best >= 0.4 else "  "
        print(f"{status} {coin:4s} | OKX ${op:8.4f} ({ok:8.0f}원) | 업비트 {up:8.0f}원 | 차익 {best:+6.2f}%", flush=True)

    except Exception as e:
        print(f"⚠️  {coin} 조회 실패", flush=True)
