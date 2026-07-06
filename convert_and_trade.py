#!/usr/bin/env python3
import ccxt, os, time, sys, io
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY'), 'enableRateLimit': True})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE'), 'enableRateLimit': True})

print("=== OKX BCH → USDT 변환 후 거래 ===\n", flush=True)

# 1. OKX BCH를 USDT로 변환
okx_bal = okx.fetch_balance()
bch = okx_bal['BCH']['free']

if bch > 0.001:
    print(f"BCH {bch:.8f}개를 USDT로 변환 중...", flush=True)
    try:
        sell = okx.create_market_sell_order('BCH/USDT', bch * 0.99)
        usdt_got = sell['cost']
        print(f"✅ ${usdt_got:.2f} USDT 확보\n", flush=True)
        time.sleep(1)
    except Exception as e:
        print(f"❌ 변환 실패: {e}", flush=True)

# 2. 거래 시작
count = 0
total = 0
MAX = 10

print("거래 시작\n", flush=True)

while count < MAX:
    try:
        for coin in ['XRP','XLM','ALGO','ID','MMT','BAT']:
            try:
                o = okx.fetch_ticker(f'{coin}/USDT')
                u = upbit.fetch_ticker(f'{coin}/KRW')

                op = o['last']
                up = u['last']
                ok = op * 1480

                pn = ((up - ok) / ok) * 100 - 0.15
                pr = ((ok - up) / up) * 100 - 0.15

                if pn >= 0.35:
                    print(f"✅ {coin} OKX→업비트 {pn:.2f}%", flush=True)

                    ob = okx.fetch_balance()
                    usdt = ob['USDT']['free'] * 0.9

                    if usdt < 0.5:
                        continue

                    print(f"OKX 매수 ${usdt:.2f}", flush=True)
                    buy = okx.create_market_buy_order(f'{coin}/USDT', usdt / op)
                    qty = buy['filled']

                    time.sleep(0.5)

                    print(f"업비트 매도 {qty:.6f}", flush=True)
                    sell = upbit.create_market_sell_order(f'{coin}/KRW', qty * 0.97)
                    krw = sell['cost']

                    profit = krw - (usdt * 1480)
                    total += profit
                    count += 1

                    print(f"✅ +{profit:.0f}원 | 누적 {total:.0f}원 ({count}/{MAX})\n", flush=True)
                    time.sleep(3)
                    break

                elif pr >= 0.35:
                    print(f"✅ {coin} 업비트→OKX {pr:.2f}%", flush=True)

                    ub = upbit.fetch_balance()
                    krw = ub['KRW']['free'] * 0.9

                    if krw < 5000:
                        continue

                    print(f"업비트 매수 {krw:.0f}원", flush=True)
                    buy = upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': krw})
                    qty = buy['filled']

                    time.sleep(0.5)

                    print(f"OKX 매도 {qty:.6f}", flush=True)
                    sell = okx.create_market_sell_order(f'{coin}/USDT', qty * 0.97)
                    usdt_got = sell['cost']

                    profit = (usdt_got * 1480) - krw
                    total += profit
                    count += 1

                    print(f"✅ +{profit:.0f}원 | 누적 {total:.0f}원 ({count}/{MAX})\n", flush=True)
                    time.sleep(3)
                    break

            except Exception as e:
                continue

        time.sleep(8)

    except KeyboardInterrupt:
        break

print(f"\n완료: {count}회, 총 {total:.0f}원", flush=True)
