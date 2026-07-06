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
MAX = 20
RATE = 1480

print("자동거래 시작\n", flush=True)

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

                if pn >= 0.4:
                    print(f"✅ {coin} OKX→업비트 {pn:.2f}%", flush=True)

                    ob = okx.fetch_balance()
                    usdt = min(ob['USDT']['free'] * 0.8, 10)

                    if usdt < 1:
                        continue

                    print(f"OKX 매수 ${usdt:.2f}", flush=True)
                    buy = okx.create_market_buy_order(f'{coin}/USDT', usdt / op)
                    qty = buy['filled']

                    time.sleep(0.5)

                    print(f"업비트 매도 {qty:.6f}", flush=True)
                    sell = upbit.create_market_sell_order(f'{coin}/KRW', qty * 0.97)
                    krw = sell['cost']

                    profit = krw - (usdt * RATE)
                    total += profit
                    count += 1

                    print(f"✅ +{profit:.0f}원 | 누적 {total:.0f}원 ({count}/{MAX})\n", flush=True)
                    time.sleep(3)
                    break

                elif pr >= 0.4:
                    print(f"✅ {coin} 업비트→OKX {pr:.2f}%", flush=True)

                    ub = upbit.fetch_balance()
                    krw = min(ub['KRW']['free'] * 0.8, 15000)

                    if krw < 5000:
                        continue

                    print(f"업비트 매수 {krw:.0f}원", flush=True)
                    buy = upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': krw})
                    qty = buy['filled']
                    print(f"수량: {qty:.6f}", flush=True)

                    time.sleep(0.5)

                    print(f"OKX 매도 {qty:.6f}", flush=True)
                    sell = okx.create_market_sell_order(f'{coin}/USDT', qty * 0.97)
                    usdt_got = sell['cost']
                    print(f"받은 금액: ${usdt_got:.2f}", flush=True)

                    profit = (usdt_got * RATE) - krw
                    total += profit
                    count += 1

                    print(f"✅ +{profit:.0f}원 | 누적 {total:.0f}원 ({count}/{MAX})\n", flush=True)
                    time.sleep(3)
                    break

            except Exception as e:
                continue

        time.sleep(10)

    except KeyboardInterrupt:
        break

print(f"\n완료: {count}회, 총 {total:.0f}원", flush=True)
