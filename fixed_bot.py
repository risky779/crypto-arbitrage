#!/usr/bin/env python3
import ccxt, os, time, sys, io
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY'), 'enableRateLimit': True})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE'), 'enableRateLimit': True})

count = 0
total = 0
MAX = 30
RATE = 1480

print("차익거래 시작\n", flush=True)

while count < MAX:
    try:
        for coin in ['XRP','XLM','ALGO','BCH','ID','MMT','BAT']:
            try:
                o = okx.fetch_ticker(f'{coin}/USDT')
                u = upbit.fetch_ticker(f'{coin}/KRW')

                op = o['last']
                up = u['last']
                ok = op * RATE

                pn = ((up - ok) / ok) * 100 - 0.15
                pr = ((ok - up) / up) * 100 - 0.15

                # OKX→업비트
                if pn >= 0.4:
                    ob = okx.fetch_balance()
                    usdt = min(ob['USDT']['free'] * 0.8, 10)

                    if usdt < 1:
                        continue

                    print(f"[{count+1}/{MAX}] {coin} OKX→업비트 {pn:.2f}%", flush=True)

                    # OKX 매수
                    buy_okx = okx.create_market_buy_order(f'{coin}/USDT', usdt / op)
                    qty = buy_okx.get('filled', 0)

                    if qty < 0.0001:
                        print(f"❌ OKX 매수 실패\n", flush=True)
                        continue

                    print(f"OKX 매수: {qty:.6f}개 (${usdt:.2f})", flush=True)
                    time.sleep(0.5)

                    # 업비트 매도
                    sell_upbit = upbit.create_market_sell_order(f'{coin}/KRW', qty * 0.97)
                    krw = sell_upbit.get('cost', 0)

                    if krw < 1000:
                        print(f"❌ 업비트 매도 실패\n", flush=True)
                        continue

                    profit = krw - (usdt * RATE)
                    total += profit
                    count += 1

                    print(f"업비트 매도: {krw:,.0f}원", flush=True)
                    print(f"✅ 수익 +{profit:.0f}원 | 누적 {total:.0f}원\n", flush=True)
                    time.sleep(3)
                    break

                # 업비트→OKX
                elif pr >= 0.4:
                    ub = upbit.fetch_balance()
                    krw = min(ub['KRW']['free'] * 0.8, 15000)

                    if krw < 5000:
                        continue

                    print(f"[{count+1}/{MAX}] {coin} 업비트→OKX {pr:.2f}%", flush=True)

                    # 업비트 매수
                    buy_upbit = upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': krw})
                    qty = buy_upbit.get('filled', 0)

                    if qty < 0.0001:
                        print(f"❌ 업비트 매수 실패\n", flush=True)
                        continue

                    print(f"업비트 매수: {qty:.6f}개 ({krw:,.0f}원)", flush=True)
                    time.sleep(0.5)

                    # OKX 매도
                    sell_okx = okx.create_market_sell_order(f'{coin}/USDT', qty * 0.97)
                    usdt_got = sell_okx.get('cost', 0)

                    if usdt_got < 0.1:
                        print(f"❌ OKX 매도 실패\n", flush=True)
                        continue

                    profit = (usdt_got * RATE) - krw
                    total += profit
                    count += 1

                    print(f"OKX 매도: ${usdt_got:.2f}", flush=True)
                    print(f"✅ 수익 +{profit:.0f}원 | 누적 {total:.0f}원\n", flush=True)
                    time.sleep(3)
                    break

            except Exception as e:
                continue

        time.sleep(15)

    except KeyboardInterrupt:
        break

print(f"\n완료: {count}회, 총 수익 {total:.0f}원", flush=True)
