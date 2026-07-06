#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
변동성 높은 코인 TOP 10 찾기
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

print("="*80, flush=True)
print("변동성 TOP 10 코인 탐색", flush=True)
print("="*80, flush=True)

# 거래소 초기화
okx = ccxt.okx({'enableRateLimit': True})
upbit = ccxt.upbit({'enableRateLimit': True})
bithumb = ccxt.bithumb({'enableRateLimit': True})

print("\n1. 공통 코인 찾는 중...", flush=True)

# OKX USDT 마켓
okx_markets = okx.load_markets()
okx_coins = set([m.replace('/USDT', '') for m in okx_markets.keys() if '/USDT' in m])

# 업비트 KRW 마켓
upbit_markets = upbit.load_markets()
upbit_coins = set([m.replace('/KRW', '') for m in upbit_markets.keys() if '/KRW' in m])

# 빗썸 KRW 마켓
bithumb_markets = bithumb.load_markets()
bithumb_coins = set([m.replace('/KRW', '') for m in bithumb_markets.keys() if '/KRW' in m])

# 3개 거래소 공통 코인
common_coins = okx_coins & upbit_coins & bithumb_coins
print(f"✅ 공통 코인 {len(common_coins)}개 발견", flush=True)

print("\n2. 변동성 분석 중...", flush=True)

volatility_data = []

for coin in common_coins:
    try:
        # 24시간 티커 정보
        okx_ticker = okx.fetch_ticker(f'{coin}/USDT')
        upbit_ticker = upbit.fetch_ticker(f'{coin}/KRW')
        bithumb_ticker = bithumb.fetch_ticker(f'{coin}/KRW')

        # 변동성 계산 (24h high/low 차이)
        okx_volatility = ((okx_ticker['high'] - okx_ticker['low']) / okx_ticker['low']) * 100 if okx_ticker['low'] else 0
        upbit_volatility = ((upbit_ticker['high'] - upbit_ticker['low']) / upbit_ticker['low']) * 100 if upbit_ticker['low'] else 0
        bithumb_volatility = ((bithumb_ticker['high'] - bithumb_ticker['low']) / bithumb_ticker['low']) * 100 if bithumb_ticker['low'] else 0

        # 평균 변동성
        avg_volatility = (okx_volatility + upbit_volatility + bithumb_volatility) / 3

        # 거래량 (OKX 기준)
        volume = okx_ticker.get('quoteVolume', 0)

        volatility_data.append({
            'coin': coin,
            'volatility': avg_volatility,
            'volume': volume,
            'okx_price': okx_ticker['last'],
            'upbit_price': upbit_ticker['last'],
        })

        print(f"  {coin}: 변동성 {avg_volatility:.2f}%", flush=True)

    except Exception as e:
        # 에러 나는 코인은 스킵
        continue

print(f"\n✅ {len(volatility_data)}개 코인 분석 완료", flush=True)

# 변동성 순으로 정렬
volatility_data.sort(key=lambda x: x['volatility'], reverse=True)

print("\n" + "="*80, flush=True)
print("🔥 변동성 TOP 10", flush=True)
print("="*80, flush=True)

top_10 = volatility_data[:10]

for i, data in enumerate(top_10, 1):
    print(f"{i:2d}. {data['coin']:6s} | 변동성: {data['volatility']:6.2f}% | 거래량: ${data['volume']:,.0f}", flush=True)

print("\n" + "="*80, flush=True)

# 파일로 저장
with open('top_volatile_coins.txt', 'w') as f:
    f.write(','.join([d['coin'] for d in top_10]))

print("✅ top_volatile_coins.txt 파일에 저장됨", flush=True)
print("\n추천 코인 리스트:", flush=True)
print(','.join([d['coin'] for d in top_10]), flush=True)
print("="*80, flush=True)
