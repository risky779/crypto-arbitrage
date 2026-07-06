#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OKX에서 BCH 매수
"""

import ccxt
import sys
import io
import os
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# OKX API
okx_api_key = os.getenv('OKX_API_KEY')
okx_secret = os.getenv('OKX_SECRET_KEY')
okx_passphrase = os.getenv('OKX_PASSPHRASE')

okx = ccxt.okx({
    'apiKey': okx_api_key,
    'secret': okx_secret,
    'password': okx_passphrase,
    'enableRateLimit': True,
})

try:
    # 1. 현재 잔고 확인
    print("="*80, flush=True)
    print("OKX BCH 매수", flush=True)
    print("="*80, flush=True)

    balance = okx.fetch_balance()
    usdt_balance = balance['USDT']['free']
    bch_balance = balance.get('BCH', {}).get('free', 0)

    print(f"\n현재 잔고:", flush=True)
    print(f"  USDT: {usdt_balance:.2f}", flush=True)
    print(f"  BCH: {bch_balance:.6f}", flush=True)

    # 2. BCH 시세 확인
    ticker = okx.fetch_ticker('BCH/USDT')
    bch_price = ticker['last']
    print(f"\nBCH 가격: ${bch_price:.2f}", flush=True)

    # 3. 매수 수량 계산 (절반 사용)
    usdt_to_use = usdt_balance * 0.5  # 절반
    bch_quantity = usdt_to_use / bch_price

    print(f"\n매수 계획:", flush=True)
    print(f"  사용 USDT: {usdt_to_use:.2f}", flush=True)
    print(f"  매수 BCH: {bch_quantity:.6f}", flush=True)
    print(f"  예상 비용: ${usdt_to_use:.2f}", flush=True)

    # 4. 5초 카운트다운
    print("\n" + "="*80, flush=True)
    for i in range(5, 0, -1):
        print(f"{i}초 후 매수... (Ctrl+C로 취소)", flush=True)
        import time
        time.sleep(1)

    # 5. 시장가 매수
    print("\n매수 중...", flush=True)
    order = okx.create_market_buy_order('BCH/USDT', bch_quantity)

    print("\n✅ 매수 완료!", flush=True)
    print(f"  주문 ID: {order['id']}", flush=True)
    print(f"  매수량: {order['filled']:.6f} BCH", flush=True)
    print(f"  평균 가격: ${order['average']:.2f}" if order.get('average') else "", flush=True)
    print(f"  총 비용: {order['cost']:.2f} USDT", flush=True)

    # 6. 최종 잔고 확인
    print("\n최종 잔고 확인 중...", flush=True)
    import time
    time.sleep(2)

    balance = okx.fetch_balance()
    final_usdt = balance['USDT']['free']
    final_bch = balance.get('BCH', {}).get('free', 0)

    print(f"\n최종 잔고:", flush=True)
    print(f"  USDT: {final_usdt:.2f}", flush=True)
    print(f"  BCH: {final_bch:.6f}", flush=True)

    print("\n" + "="*80, flush=True)
    print("✅ 준비 완료! 이제 양방향 거래 봇을 실행하세요:", flush=True)
    print("   start_two_way_trade.bat", flush=True)
    print("="*80, flush=True)

except Exception as e:
    print(f"\n❌ 오류: {e}", flush=True)
