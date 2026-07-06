#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
양방향 포지션 구성
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

# API 초기화
upbit = ccxt.upbit({
    'apiKey': os.getenv('UPBIT_ACCESS_KEY'),
    'secret': os.getenv('UPBIT_SECRET_KEY'),
    'enableRateLimit': True,
})

try:
    print("="*80, flush=True)
    print("양방향 포지션 구성", flush=True)
    print("="*80, flush=True)

    # 현재 잔고
    balance = upbit.fetch_balance()
    krw = balance['KRW']['free']
    bch = balance.get('BCH', {}).get('free', 0)

    print(f"\n현재 업비트 잔고:", flush=True)
    print(f"  KRW: {krw:,.0f}원", flush=True)
    print(f"  BCH: {bch:.6f}", flush=True)

    # BCH 시세
    ticker = upbit.fetch_ticker('BCH/KRW')
    bch_price = ticker['last']
    print(f"\nBCH 가격: {bch_price:,.0f}원", flush=True)

    # 절반으로 BCH 매수
    krw_to_use = krw * 0.5
    bch_to_buy = krw_to_use / bch_price

    print(f"\n매수 계획:", flush=True)
    print(f"  사용 KRW: {krw_to_use:,.0f}원 (50%)", flush=True)
    print(f"  매수 BCH: {bch_to_buy:.6f}", flush=True)
    print(f"  남은 KRW: {krw * 0.5:,.0f}원 (50%)", flush=True)

    print(f"\n양방향 포지션 준비:", flush=True)
    print(f"  ✅ 정프리미엄 대응: OKX BCH 매도 + 업비트 BCH 매수", flush=True)
    print(f"  ✅ 역프리미엄 대응: 업비트 BCH 매도 + OKX BCH 매수", flush=True)

    # 5초 카운트다운
    print("\n" + "="*80, flush=True)
    for i in range(5, 0, -1):
        print(f"{i}초 후 매수... (Ctrl+C로 취소)", flush=True)
        import time
        time.sleep(1)

    # 매수 (업비트는 cost 기준)
    print("\n매수 중...", flush=True)
    order = upbit.create_order('BCH/KRW', 'market', 'buy', None, None, {'cost': krw_to_use})

    print(f"\n✅ 매수 완료!", flush=True)
    print(f"  매수량: {order['filled']:.6f} BCH", flush=True)

    # 최종 잔고
    time.sleep(2)
    balance = upbit.fetch_balance()
    final_krw = balance['KRW']['free']
    final_bch = balance.get('BCH', {}).get('free', 0)

    print(f"\n최종 업비트 잔고:", flush=True)
    print(f"  KRW: {final_krw:,.0f}원", flush=True)
    print(f"  BCH: {final_bch:.6f}", flush=True)

    print("\n" + "="*80, flush=True)
    print("✅ 양방향 포지션 준비 완료!", flush=True)
    print("="*80, flush=True)

except Exception as e:
    print(f"\n❌ 오류: {e}", flush=True)
