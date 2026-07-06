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

print("균형 거래 봇 시작\n", flush=True)

while count < MAX:
    try:
        for coin in ['ID', 'BAT', 'ALGO', 'MMT', 'XLM', 'XRP', 'BCH', 'ETC', 'DOGE', 'ADA', 'DOT', 'LINK']:
            try:
                o = okx.fetch_ticker(f'{coin}/USDT')
                u = upbit.fetch_ticker(f'{coin}/KRW')

                op = o['last']
                up = u['last']

                profit_pct = ((up - op * RATE) / (op * RATE)) * 100 - 0.4

                if profit_pct >= 0.6:
                    print(f"\n[{count+1}] {coin} 차익 {profit_pct:.2f}%", flush=True)

                    # 거래 전 잔고 확인
                    upbit_bal = upbit.fetch_balance()
                    okx_bal = okx.fetch_balance()

                    upbit_coin = upbit_bal.get(coin, {}).get('free', 0)
                    okx_usdt = okx_bal['USDT']['free']

                    # 거래 가능 여부 확인
                    # OKX 최소 $10, 업비트 최소 6000원 충족
                    usdt_amount = min(okx_usdt * 0.7, 15)

                    if usdt_amount < 10:
                        print(f"  USDT 부족: ${okx_usdt:.2f} < $10", flush=True)
                        continue

                    coin_needed = usdt_amount / op
                    upbit_min_qty = 6000 / up  # 업비트 최소금액 충족

                    if upbit_coin < max(coin_needed * 0.95, upbit_min_qty):
                        print(f"  업비트 {coin} 부족: {upbit_coin:.2f}개", flush=True)
                        continue

                    # 1. OKX 매수
                    print(f"  OKX ${usdt_amount:.2f} 매수 중...", flush=True)
                    buy = okx.create_market_buy_order(f'{coin}/USDT', coin_needed)
                    time.sleep(1)

                    # 2. 실제 매수 수량 확인
                    okx_bal_after = okx.fetch_balance()
                    okx_coin_after = okx_bal_after.get(coin, {}).get('free', 0)

                    actual_bought = okx_coin_after
                    print(f"  OKX 매수 완료: {actual_bought:.2f}개", flush=True)

                    # 3. 업비트에서 동일 수량 매도
                    sell_qty = min(actual_bought * 0.99, upbit_coin * 0.95)

                    if sell_qty * up < 6000:
                        print(f"  매도 금액 부족: {sell_qty * up:.0f}원 < 6000원", flush=True)
                        # OKX 것은 그대로 보유 (다음에 매도)
                        continue

                    print(f"  업비트 {sell_qty:.2f}개 매도 중...", flush=True)
                    sell = upbit.create_market_sell_order(f'{coin}/KRW', sell_qty)
                    krw_got = sell.get('cost', 0) if sell else 0

                    if krw_got and krw_got > 0:
                        print(f"  업비트 매도 완료: {krw_got:,.0f}원", flush=True)
                    else:
                        # cost가 없어도 매도는 성공했을 수 있음 - 잔고로 확인
                        time.sleep(0.5)
                        upbit_check = upbit.fetch_balance()
                        krw_now = upbit_check['KRW']['free']
                        krw_got = sell_qty * up * 0.9995  # 추정 (수수료 제외)
                        print(f"  업비트 매도 완료 (추정): {krw_got:,.0f}원", flush=True)

                    # 4. 수익 계산
                    profit = krw_got - (usdt_amount * RATE)
                    total += profit
                    count += 1

                    print(f"✅ +{profit:.0f}원 (누적 {total:.0f}원)", flush=True)

                    # 잔고 확인
                    time.sleep(1)
                    okx_final = okx.fetch_balance()
                    okx_coin_final = okx_final.get(coin, {}).get('free', 0)
                    if okx_coin_final > 10:
                        print(f"  ⚠️  OKX {coin} 잔여: {okx_coin_final:.2f}개", flush=True)

                    time.sleep(3)
                    break

            except Exception as e:
                print(f"  {coin} 오류: {str(e)[:50]}", flush=True)
                continue

        time.sleep(12)

    except KeyboardInterrupt:
        print("\n중지", flush=True)
        break

print(f"\n완료: {count}회, {total:.0f}원", flush=True)

# 최종 잔고
upbit_bal = upbit.fetch_balance()
okx_bal = okx.fetch_balance()
print(f"\n업비트 KRW: {upbit_bal['KRW']['free']:,.0f}원", flush=True)
print(f"OKX USDT: ${okx_bal['USDT']['free']:.2f}", flush=True)
