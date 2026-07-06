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
MAX = 50
RATE = 1480

print("차익거래 시작\n", flush=True)

while count < MAX:
    try:
        for coin in ['ID','BAT','ALGO','MMT','XLM','XRP','BCH']:
            try:
                o = okx.fetch_ticker(f'{coin}/USDT')
                u = upbit.fetch_ticker(f'{coin}/KRW')

                op = o['last']
                up = u['last']
                ok = op * RATE

                pn = ((up - ok) / ok) * 100 - 0.2
                pr = ((ok - up) / up) * 100 - 0.2

                # OKX→업비트
                if pn >= 0.4:
                    ob = okx.fetch_balance()
                    usdt = min(ob['USDT']['free'] * 0.75, 8)

                    if usdt < 1:
                        continue

                    print(f"[{count+1}] {coin} OKX→업비트 {pn:.2f}%", flush=True)

                    # 1. OKX 매수
                    buy = okx.create_market_buy_order(f'{coin}/USDT', usdt / op)
                    qty = buy.get('filled', 0)

                    if qty < 0.0001:
                        print(f"❌ OKX 매수 실패\n", flush=True)
                        continue

                    print(f"  OKX 매수 성공: {qty:.6f}개", flush=True)

                    # OKX 실제 잔고 재확인
                    time.sleep(0.5)
                    okx_bal = okx.fetch_balance()
                    actual_qty = okx_bal.get(coin, {}).get('free', 0)
                    if actual_qty > qty * 0.9:
                        qty = actual_qty
                        print(f"  실제 보유: {qty:.6f}개", flush=True)
                    time.sleep(1)

                    # 2. 업비트 전량 매도
                    sell = upbit.create_market_sell_order(f'{coin}/KRW', qty)
                    krw = sell['cost']

                    if not krw or krw < 1000:
                        print(f"❌ 업비트 매도 실패 - OKX에 {qty:.6f}개 남음!\n", flush=True)
                        continue

                    profit = krw - (usdt * RATE)
                    total += profit
                    count += 1

                    print(f"  업비트 매도: {krw:,.0f}원", flush=True)
                    print(f"✅ +{profit:.0f}원 (누적 {total:.0f}원)\n", flush=True)
                    time.sleep(2)
                    break

                # 업비트→OKX
                elif pr >= 0.4:
                    ub = upbit.fetch_balance()
                    krw = min(ub['KRW']['free'] * 0.75, 12000)

                    if krw < 5000:
                        continue

                    print(f"[{count+1}] {coin} 업비트→OKX {pr:.2f}%", flush=True)

                    # 1. 업비트 매수
                    buy = upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': krw})
                    qty = buy.get('filled', 0)

                    if qty < 0.0001:
                        print(f"❌ 업비트 매수 실패\n", flush=True)
                        continue

                    print(f"  업비트 매수 성공: {qty:.6f}개", flush=True)

                    # 업비트 실제 잔고 재확인
                    time.sleep(0.5)
                    upbit_bal = upbit.fetch_balance()
                    actual_qty = upbit_bal.get(coin, {}).get('free', 0)
                    if actual_qty > qty * 0.9:
                        qty = actual_qty
                        print(f"  실제 보유: {qty:.6f}개", flush=True)
                    time.sleep(1)

                    # 2. OKX 전량 매도
                    sell = okx.create_market_sell_order(f'{coin}/USDT', qty)
                    usdt_got = sell['cost']

                    if not usdt_got or usdt_got < 0.1:
                        print(f"❌ OKX 매도 실패 - 업비트에 {qty:.6f}개 남음!\n", flush=True)
                        continue

                    profit = (usdt_got * RATE) - krw
                    total += profit
                    count += 1

                    print(f"  OKX 매도: ${usdt_got:.2f}", flush=True)
                    print(f"✅ +{profit:.0f}원 (누적 {total:.0f}원)\n", flush=True)
                    time.sleep(2)
                    break

            except Exception as e:
                time.sleep(1)
                continue

        time.sleep(12)

    except KeyboardInterrupt:
        print("\n중지됨", flush=True)
        break

print(f"\n완료: {count}회 거래, 총 {total:.0f}원 수익", flush=True)
