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
print("=== 최적 포지션 분석 ===\n", flush=True)

# 현재 잔고
print("현재 자산:", flush=True)
print(f"  업비트: 45,660원", flush=True)
print(f"  OKX: $49.10 (72,668원)\n", flush=True)

coins = ['ID', 'BAT', 'ALGO', 'MMT', 'XLM']

print("전략 A: 업비트에 코인 보유", flush=True)
print("=" * 50, flush=True)
for coin in coins:
    try:
        o = okx.fetch_ticker(f'{coin}/USDT')
        u = upbit.fetch_ticker(f'{coin}/KRW')

        op = o['last']
        up = u['last']

        # 업비트에 30,000원 매수
        upbit_qty = 30000 / up

        # OKX→업비트: OKX 매수 후 업비트 매도
        okx_to_upbit = ((up - op * RATE) / (op * RATE)) * 100 - 0.2

        # 업비트→OKX: 업비트 매수 후 OKX 매도 (불가능 - 이미 보유)
        upbit_to_okx = "불가능 (이미 보유)"

        print(f"{coin}:", flush=True)
        print(f"  업비트 30,000원 = {upbit_qty:.2f}개", flush=True)
        print(f"  OKX→업비트 차익: {okx_to_upbit:+.2f}%", flush=True)
        print(f"  업비트→OKX 차익: {upbit_to_okx}", flush=True)
        print()
    except:
        continue

print("\n전략 B: OKX에 코인 보유", flush=True)
print("=" * 50, flush=True)
for coin in coins:
    try:
        o = okx.fetch_ticker(f'{coin}/USDT')
        u = upbit.fetch_ticker(f'{coin}/KRW')

        op = o['last']
        up = u['last']

        # OKX에 $30 매수
        okx_qty = 30 / op

        # OKX→업비트: OKX 매도 후 업비트 매수 (불가능 - 이미 보유)
        okx_to_upbit = "불가능 (이미 보유)"

        # 업비트→OKX: 업비트 매수 후 OKX 매도
        upbit_to_okx = ((op * RATE - up) / up) * 100 - 0.2

        print(f"{coin}:", flush=True)
        print(f"  OKX $30 = {okx_qty:.2f}개", flush=True)
        print(f"  OKX→업비트 차익: {okx_to_upbit}", flush=True)
        print(f"  업비트→OKX 차익: {upbit_to_okx:+.2f}%", flush=True)
        print()
    except:
        continue

print("\n결론:", flush=True)
print("- 최근 ID가 OKX→업비트 방향으로 차익 발생", flush=True)
print("- 전략 A(업비트에 ID 보유) 추천", flush=True)
print("- 업비트에서 ID 30,000원 매수하면", flush=True)
print("  차익 발생 시: OKX에서 ID 매수 → 업비트에서 ID 매도", flush=True)
