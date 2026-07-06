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
MAX = 10

print("시작\n", flush=True)

while count < MAX:
    try:
        for coin in ['XRP','XLM','ALGO','BCH','ID','MMT','BAT']:
            try:
                o = okx.fetch_ticker(f'{coin}/USDT')
                u = upbit.fetch_ticker(f'{coin}/KRW')

                op = o['last']
                up = u['last']
                ok = op * 1480

                pn = ((up - ok) / ok) * 100 - 0.15
                pr = ((ok - up) / up) * 100 - 0.15

                print(f"{coin}: OKX {op:.4f} ({ok:.0f}원) | 업비트 {up:.0f}원 | 차익 {pn:+.2f}%", flush=True)

                if pn >= 0.35:
                    print(f"\n✅ {coin} OKX→업비트 {pn:.2f}%", flush=True)

                    ob = okx.fetch_balance()
                    usdt = min(ob['USDT']['free'] * 0.75, 8)

                    if usdt < 1:
                        print("USDT 부족", flush=True)
                        continue

                    print(f"OKX 매수 ${usdt:.2f}", flush=True)
                    buy = okx.create_market_buy_order(f'{coin}/USDT', usdt / op)
                    qty = buy['filled']
                    print(f"수량: {qty:.6f}", flush=True)

                    time.sleep(0.5)

                    print(f"업비트 매도", flush=True)
                    sell = upbit.create_market_sell_order(f'{coin}/KRW', qty * 0.97)
                    krw = sell['cost']

                    profit = krw - (usdt * 1480)
                    total += profit
                    count += 1

                    print(f"✅ +{profit:.0f}원 | 누적: {total:.0f}원 ({count}/{MAX})\n", flush=True)
                    time.sleep(3)
                    break

                elif pr >= 0.35:
                    print(f"\n✅ {coin} 업비트→OKX {pr:.2f}%", flush=True)

                    ub = upbit.fetch_balance()
                    krw = min(ub['KRW']['free'] * 0.75, 12000)

                    if krw < 5000:
                        print("KRW 부족", flush=True)
                        continue

                    print(f"업비트 매수 {krw:.0f}원", flush=True)
                    buy = upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': krw})
                    qty = buy['filled']
                    print(f"수량: {qty:.6f}", flush=True)

                    time.sleep(0.5)

                    print(f"OKX 매도", flush=True)
                    sell = okx.create_market_sell_order(f'{coin}/USDT', qty * 0.97)
                    usdt_got = sell['cost']

                    profit = (usdt_got * 1480) - krw
                    total += profit
                    count += 1

                    print(f"✅ +{profit:.0f}원 | 누적: {total:.0f}원 ({count}/{MAX})\n", flush=True)
                    time.sleep(3)
                    break

            except Exception as e:
                continue

        time.sleep(8)

    except KeyboardInterrupt:
        break
    except Exception as e:
        time.sleep(5)

print(f"\n완료: {count}회, {total:.0f}원", flush=True)
