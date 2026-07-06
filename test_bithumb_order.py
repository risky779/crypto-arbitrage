#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
빗썸 주문 API 테스트
"""
from bithumb_api_v2 import BithumbAPIv2

api = BithumbAPIv2()

print("=== 빗썸 주문 테스트 ===\n")

# 1. 잔고 확인
print("1. 잔고 확인:")
balance = api.get_balance()
krw = balance.get('KRW', {}).get('free', 0)
print(f"사용 가능 KRW: {krw:,.0f}원\n")

# 2. 최소 주문 금액으로 매수 테스트 (5000원)
print("2. BAT 매수 테스트 (5000원):")
try:
    result = api.market_buy('KRW-BAT', 5000)
    print(f"✅ 매수 성공!")
    print(f"주문 ID: {result.get('uuid')}")
    print(f"주문 상태: {result.get('state')}")
except Exception as e:
    print(f"❌ 매수 실패: {e}")
