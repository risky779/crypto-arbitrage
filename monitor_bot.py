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

print("모니터링 시작\n", flush=True)

while count < MAX:
    try:
        for coin in ['ID','BAT','ALGO','MMT','XLM']:
            try:
                o = okx.fetch_ticker(f'{coin}/USDT')
                u = upbit.fetch_ticker(f'{coin}/KRW')

                op = o['last']
                up = u['last']
                ok = op * RATE

                pn = ((up - ok) / ok) * 100 - 0.2
                pr = ((ok - up) / up) * 100 - 0.2

                # OKX→업비트 (OKX 매수 + 업비트 매도)
                if pn >= 0.4:
                    print(f"\n[{count+1}] {coin} 차익 {pn:.2f}%", flush=True)

                    # OKX 매수
                    usdt = min(okx.fetch_balance()['USDT']['free'] * 0.7, 8)
                    if usdt < 1:
                        continue

                    print(f"  OKX ${usdt:.2f} 매수...", flush=True)
                    okx.create_market_buy_order(f'{coin}/USDT', usdt / op)
                    time.sleep(1)

                    # 업비트 매도
                    qty = upbit.fetch_balance().get(coin, {}).get('free', 0)
                    if qty < 0.01:
                        print(f"  ❌ 업비트 {coin} 부족\n", flush=True)
                        continue

                    sell_qty = min(qty * 0.95, usdt / op * 1.5)
                    print(f"  업비트 {sell_qty:.4f}개 매도...", flush=True)
                    sell = upbit.create_market_sell_order(f'{coin}/KRW', sell_qty)
                    krw = sell.get('cost', 0)

                    profit = krw - (usdt * RATE)
                    total += profit
                    count += 1

                    print(f"✅ +{profit:.0f}원 (누적 {total:.0f}원)\n", flush=True)
                    time.sleep(2)
                    break

                # 업비트→OKX (업비트 매수 + OKX 매도)
                elif pr >= 0.4:
                    print(f"\n[{count+1}] {coin} 차익 {pr:.2f}%", flush=True)

                    # 업비트 매수
                    krw = min(upbit.fetch_balance()['KRW']['free'] * 0.7, 10000)
                    if krw < 5000:
                        continue

                    print(f"  업비트 {krw:,.0f}원 매수...", flush=True)
                    upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': krw})
                    time.sleep(1)

                    # OKX 매도
                    qty = okx.fetch_balance().get(coin, {}).get('free', 0)
                    if qty < 0.01:
                        print(f"  ❌ OKX {coin} 부족\n", flush=True)
                        continue

                    sell_qty = min(qty * 0.95, krw / up * 1.5)
                    print(f"  OKX {sell_qty:.4f}개 매도...", flush=True)
                    sell = okx.create_market_sell_order(f'{coin}/USDT', sell_qty)
                    usdt_got = sell.get('cost', 0)

                    profit = (usdt_got * RATE) - krw
                    total += profit
                    count += 1

                    print(f"✅ +{profit:.0f}원 (누적 {total:.0f}원)\n", flush=True)
                    time.sleep(2)
                    break

            except Exception as e:
                continue

        time.sleep(15)

    except KeyboardInterrupt:
        print("\n중지", flush=True)
        break

print(f"\n완료: {count}회, {total:.0f}원", flush=True)
