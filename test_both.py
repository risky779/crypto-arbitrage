#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY')})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})

print("=== 양쪽 거래소 테스트 ===\n", flush=True)

# 1. OKX 매수 테스트
print("1. OKX ID $1 매수 테스트", flush=True)
try:
    okx_before = okx.fetch_balance()
    usdt_before = okx_before['USDT']['free']
    id_before = okx_before.get('ID', {}).get('free', 0)

    print(f"  매수 전 - USDT: ${usdt_before:.2f}, ID: {id_before:.2f}개", flush=True)

    result = okx.create_market_buy_order('ID/USDT', 1)
    print(f"  결과 타입: {type(result)}", flush=True)
    print(f"  결과: {result}", flush=True)

    time.sleep(1)
    okx_after = okx.fetch_balance()
    usdt_after = okx_after['USDT']['free']
    id_after = okx_after.get('ID', {}).get('free', 0)

    print(f"  매수 후 - USDT: ${usdt_after:.2f}, ID: {id_after:.2f}개", flush=True)
    print(f"  ✅ OKX 매수 성공: {id_after - id_before:.2f}개\n", flush=True)

except Exception as e:
    print(f"  ❌ OKX 매수 실패: {e}\n", flush=True)

# 2. 업비트 매도 테스트
print("2. 업비트 ID 20개 매도 테스트", flush=True)
try:
    upbit_before = upbit.fetch_balance()
    krw_before = upbit_before['KRW']['free']
    id_before = upbit_before.get('ID', {}).get('free', 0)

    print(f"  매도 전 - KRW: {krw_before:,.0f}원, ID: {id_before:.2f}개", flush=True)

    ticker = upbit.fetch_ticker('ID/KRW')
    print(f"  ID 현재가: {ticker['last']}원", flush=True)
    print(f"  20개 예상 금액: {20 * ticker['last']:,.0f}원", flush=True)

    result = upbit.create_market_sell_order('ID/KRW', 20)
    print(f"  결과 타입: {type(result)}", flush=True)
    print(f"  결과: {result}", flush=True)

    time.sleep(1)
    upbit_after = upbit.fetch_balance()
    krw_after = upbit_after['KRW']['free']
    id_after = upbit_after.get('ID', {}).get('free', 0)

    print(f"  매도 후 - KRW: {krw_after:,.0f}원, ID: {id_after:.2f}개", flush=True)
    print(f"  ✅ 업비트 매도 성공: {krw_after - krw_before:,.0f}원\n", flush=True)

except Exception as e:
    print(f"  ❌ 업비트 매도 실패: {e}\n", flush=True)

print("테스트 완료", flush=True)
