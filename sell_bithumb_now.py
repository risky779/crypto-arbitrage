#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
빗썸 보유 코인 즉시 매도
"""
import sys
import io
from bithumb_api_v2 import BithumbAPIv2

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

api = BithumbAPIv2()

print("=== 빗썸 보유 코인 즉시 매도 ===\n")

# 1. 현재 잔고 확인
balance = api.get_balance()
coins_to_sell = []

for coin, info in balance.items():
    if coin != 'KRW':
        free = info.get('free', 0)
        if free > 0.0001:
            coins_to_sell.append((coin, free))

if not coins_to_sell:
    print("매도할 코인이 없습니다.")
    exit(0)

print(f"매도할 코인: {len(coins_to_sell)}개\n")

initial_krw = balance.get('KRW', {}).get('free', 0)
print(f"매도 전 KRW: {initial_krw:,.0f}원\n")

# 2. 각 코인 매도
for coin, amount in coins_to_sell:
    print(f"{'='*50}")
    print(f"💰 {coin} 매도 중... ({amount:.8f})")

    try:
        result = api.market_sell(f'KRW-{coin}', amount)
        print(f"   ✅ 매도 성공!")
        print(f"   주문 ID: {result.get('uuid', 'N/A')}")
    except Exception as e:
        print(f"   ❌ 매도 실패: {e}")

print(f"\n{'='*50}")

# 3. 최종 잔고 확인
import time
time.sleep(2)

final_balance = api.get_balance()
final_krw = final_balance.get('KRW', {}).get('free', 0)

print(f"\n=== 매도 완료 ===")
print(f"매도 후 KRW: {final_krw:,.0f}원")
print(f"순수익: {final_krw - initial_krw:,.0f}원")
