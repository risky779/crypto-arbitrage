#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bithumb_api_v2 import BithumbAPIv2

api = BithumbAPIv2()
balance = api.get_balance()

print("=== 빗썸 잔고 ===")
print(f"KRW: {balance.get('KRW', {}).get('free', 0):,.0f}원")
print(f"\n보유 코인:")
for coin, info in balance.items():
    if coin != 'KRW':
        total = info.get('free', 0) + info.get('locked', 0)
        if total > 0:
            print(f"  {coin}: {total:.8f} (free: {info.get('free', 0)}, locked: {info.get('locked', 0)})")
