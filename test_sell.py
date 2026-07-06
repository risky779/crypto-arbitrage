#!/usr/bin/env python3
import ccxt, os, sys, io
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY')})

print("=== 업비트 매도 테스트 ===\n", flush=True)

# 현재 ID 잔고
bal = upbit.fetch_balance()
id_qty = bal.get('ID', {}).get('free', 0)

print(f"현재 ID: {id_qty:.2f}개", flush=True)

if id_qty < 10:
    print("테스트할 수량 부족", flush=True)
else:
    # 소량 매도 테스트
    test_qty = 10
    print(f"\n{test_qty}개 매도 테스트...", flush=True)

    try:
        result = upbit.create_market_sell_order('ID/KRW', test_qty)
        print(f"결과 타입: {type(result)}", flush=True)
        print(f"결과 내용: {result}", flush=True)

        if result:
            cost = result.get('cost', None)
            filled = result.get('filled', None)
            print(f"\ncost: {cost}", flush=True)
            print(f"filled: {filled}", flush=True)

            if cost:
                print(f"\n✅ 매도 성공: {cost:,.0f}원", flush=True)
            else:
                print(f"\n❌ cost가 None", flush=True)
        else:
            print("\n❌ result가 None", flush=True)

    except Exception as e:
        print(f"\n❌ 오류: {e}", flush=True)
        print(f"오류 타입: {type(e)}", flush=True)

# 최종 잔고
bal = upbit.fetch_balance()
id_qty_after = bal.get('ID', {}).get('free', 0)
print(f"\n최종 ID: {id_qty_after:.2f}개", flush=True)
