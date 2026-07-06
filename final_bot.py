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

print("차익거래 시작 (ID 전용)\n", flush=True)

while count < MAX:
    try:
        coin = 'ID'

        o = okx.fetch_ticker(f'{coin}/USDT')
        u = upbit.fetch_ticker(f'{coin}/KRW')

        op = o['last']
        up = u['last']
        ok = op * RATE

        # OKX→업비트 차익 (OKX 싸면 OKX 매수 + 업비트 매도)
        profit_pct = ((up - ok) / ok) * 100 - 0.2

        if profit_pct >= 0.4:
            print(f"[{count+1}] {coin} 차익 {profit_pct:.2f}%", flush=True)

            # OKX 매수
            usdt = min(okx.fetch_balance()['USDT']['free'] * 0.8, 8)
            if usdt < 1:
                print("  OKX USDT 부족\n", flush=True)
                time.sleep(15)
                continue

            print(f"  OKX ${usdt:.2f} 매수...", flush=True)
            buy = okx.create_market_buy_order(f'{coin}/USDT', usdt / op)
            time.sleep(1)

            # 업비트 동일 수량 매도
            sell_qty = usdt / op * 0.98
            upbit_bal = upbit.fetch_balance()
            available = upbit_bal.get(coin, {}).get('free', 0)

            if available < sell_qty:
                print(f"  ❌ 업비트 {coin} 부족 ({available:.2f}개)\n", flush=True)
                time.sleep(15)
                continue

            print(f"  업비트 {sell_qty:.2f}개 매도...", flush=True)
            sell = upbit.create_market_sell_order(f'{coin}/KRW', sell_qty)
            krw = sell.get('cost', 0)

            profit = krw - (usdt * RATE)
            total += profit
            count += 1

            print(f"✅ +{profit:.0f}원 (누적 {total:.0f}원)\n", flush=True)
            time.sleep(3)

        time.sleep(15)

    except KeyboardInterrupt:
        print("\n중지", flush=True)
        break
    except Exception as e:
        time.sleep(2)
        continue

print(f"\n완료: {count}회, {total:.0f}원", flush=True)
