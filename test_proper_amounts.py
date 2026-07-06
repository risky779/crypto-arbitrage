#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY')})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})

print("=== 적절한 금액으로 양쪽 거래소 테스트 ===\n", flush=True)

# 현재 잔고
print("현재 잔고:", flush=True)
upbit_bal = upbit.fetch_balance()
okx_bal = okx.fetch_balance()

print(f"  업비트 KRW: {upbit_bal['KRW']['free']:,.0f}원", flush=True)
print(f"  업비트 ID: {upbit_bal.get('ID', {}).get('free', 0):.2f}개", flush=True)
print(f"  OKX USDT: ${okx_bal['USDT']['free']:.2f}", flush=True)
print(f"  OKX ID: {okx_bal.get('ID', {}).get('free', 0):.2f}개\n", flush=True)

# ID 현재가 확인
okx_ticker = okx.fetch_ticker('ID/USDT')
upbit_ticker = upbit.fetch_ticker('ID/KRW')
okx_price = okx_ticker['last']
upbit_price = upbit_ticker['last']

print(f"ID 현재가:", flush=True)
print(f"  OKX: ${okx_price}", flush=True)
print(f"  업비트: {upbit_price}원\n", flush=True)

# 최소 주문 금액 계산
upbit_min_qty = 5000 / upbit_price  # 업비트 5000원 충족
okx_min_usdt = 10  # OKX 최소 $10 (추정)
okx_min_qty = okx_min_usdt / okx_price

print(f"최소 주문 수량:", flush=True)
print(f"  업비트: {upbit_min_qty:.2f}개 (5000원 충족)", flush=True)
print(f"  OKX: {okx_min_qty:.2f}개 (${okx_min_usdt} 충족)\n", flush=True)

# 1. OKX 매수 테스트 ($10)
print("=" * 50, flush=True)
print("1. OKX $10 매수 테스트", flush=True)
print("=" * 50, flush=True)

if okx_bal['USDT']['free'] < 10:
    print(f"❌ USDT 부족: ${okx_bal['USDT']['free']:.2f} < $10\n", flush=True)
else:
    try:
        okx_before = okx.fetch_balance()
        usdt_before = okx_before['USDT']['free']
        id_before = okx_before.get('ID', {}).get('free', 0)

        print(f"매수 전 - USDT: ${usdt_before:.2f}, ID: {id_before:.2f}개", flush=True)

        # $10 어치 매수
        buy_qty = 10 / okx_price
        print(f"${10} 매수 시도 (약 {buy_qty:.2f}개)...", flush=True)

        result = okx.create_market_buy_order('ID/USDT', buy_qty)
        print(f"✅ 주문 성공", flush=True)
        print(f"  응답: {result}", flush=True)

        time.sleep(1)
        okx_after = okx.fetch_balance()
        usdt_after = okx_after['USDT']['free']
        id_after = okx_after.get('ID', {}).get('free', 0)

        print(f"매수 후 - USDT: ${usdt_after:.2f}, ID: {id_after:.2f}개", flush=True)
        print(f"실제 매수: {id_after - id_before:.2f}개", flush=True)
        print(f"사용 금액: ${usdt_before - usdt_after:.2f}\n", flush=True)

    except Exception as e:
        print(f"❌ 오류: {e}", flush=True)
        print(f"오류 타입: {type(e).__name__}\n", flush=True)

# 2. 업비트 매도 테스트 (5000원 이상)
print("=" * 50, flush=True)
print("2. 업비트 매도 테스트 (5000원 이상)", flush=True)
print("=" * 50, flush=True)

upbit_bal = upbit.fetch_balance()
id_available = upbit_bal.get('ID', {}).get('free', 0)

# 5000원 충족하는 수량 (여유있게 6000원)
sell_qty = 6000 / upbit_price

if id_available < sell_qty:
    print(f"❌ ID 부족: {id_available:.2f}개 < {sell_qty:.2f}개 필요\n", flush=True)
else:
    try:
        upbit_before = upbit.fetch_balance()
        krw_before = upbit_before['KRW']['free']
        id_before = upbit_before.get('ID', {}).get('free', 0)

        print(f"매도 전 - KRW: {krw_before:,.0f}원, ID: {id_before:.2f}개", flush=True)
        print(f"{sell_qty:.2f}개 매도 시도 (약 {sell_qty * upbit_price:,.0f}원)...", flush=True)

        result = upbit.create_market_sell_order('ID/KRW', sell_qty)
        print(f"✅ 주문 성공", flush=True)
        print(f"  응답: {result}", flush=True)

        time.sleep(1)
        upbit_after = upbit.fetch_balance()
        krw_after = upbit_after['KRW']['free']
        id_after = upbit_after.get('ID', {}).get('free', 0)

        print(f"매도 후 - KRW: {krw_after:,.0f}원, ID: {id_after:.2f}개", flush=True)
        print(f"실제 매도: {id_before - id_after:.2f}개", flush=True)
        print(f"받은 금액: {krw_after - krw_before:,.0f}원\n", flush=True)

    except Exception as e:
        print(f"❌ 오류: {e}", flush=True)
        print(f"오류 타입: {type(e).__name__}\n", flush=True)

print("=" * 50, flush=True)
print("테스트 완료", flush=True)
print("=" * 50, flush=True)
