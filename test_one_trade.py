#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY')})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})

RATE = 1480

print("=== 1회 테스트 거래 ===\n", flush=True)

for coin in ['ID','BAT','ALGO','MMT']:
    try:
        o = okx.fetch_ticker(f'{coin}/USDT')
        u = upbit.fetch_ticker(f'{coin}/KRW')

        op = o['last']
        up = u['last']
        ok = op * RATE

        pn = ((up - ok) / ok) * 100 - 0.2
        pr = ((ok - up) / up) * 100 - 0.2

        print(f"{coin}: OKX→업비트 {pn:.2f}% | 업비트→OKX {pr:.2f}%", flush=True)

        # OKX→업비트
        if pn >= 0.4:
            print(f"\n✅ {coin} OKX→업비트 거래 시도 ({pn:.2f}%)\n", flush=True)

            # 1. OKX 매수
            usdt = 5
            print(f"1단계: OKX ${usdt} 매수...", flush=True)
            buy = okx.create_market_buy_order(f'{coin}/USDT', usdt / op)

            time.sleep(1)
            okx_bal = okx.fetch_balance()
            qty = okx_bal.get(coin, {}).get('free', 0)

            print(f"  매수 완료: {qty:.6f}개", flush=True)

            if qty < 0.001:
                print("  ❌ 매수 실패\n", flush=True)
                break

            # 2. 업비트 매도
            print(f"2단계: 업비트 {qty:.6f}개 매도...", flush=True)
            sell = upbit.create_market_sell_order(f'{coin}/KRW', qty)
            krw = sell.get('cost', 0)

            print(f"  매도 완료: {krw:,.0f}원", flush=True)

            profit = krw - (usdt * RATE)
            print(f"\n✅ 거래 완료: {profit:,.0f}원 {'수익' if profit > 0 else '손실'}\n", flush=True)
            break

        # 업비트→OKX
        elif pr >= 0.4:
            print(f"\n✅ {coin} 업비트→OKX 거래 시도 ({pr:.2f}%)\n", flush=True)

            # 1. 업비트 매수
            krw = 10000
            print(f"1단계: 업비트 {krw:,}원 매수...", flush=True)
            buy = upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': krw})

            time.sleep(1)
            upbit_bal = upbit.fetch_balance()
            qty = upbit_bal.get(coin, {}).get('free', 0)

            print(f"  매수 완료: {qty:.6f}개", flush=True)

            if qty < 0.001:
                print("  ❌ 매수 실패\n", flush=True)
                break

            # 2. OKX 매도
            print(f"2단계: OKX {qty:.6f}개 매도...", flush=True)
            sell = okx.create_market_sell_order(f'{coin}/USDT', qty)
            usdt_got = sell.get('cost', 0)

            print(f"  매도 완료: ${usdt_got:.2f}", flush=True)

            profit = (usdt_got * RATE) - krw
            print(f"\n✅ 거래 완료: {profit:,.0f}원 {'수익' if profit > 0 else '손실'}\n", flush=True)
            break

    except Exception as e:
        print(f"{coin} 오류: {e}\n", flush=True)
        continue

print("테스트 종료", flush=True)
