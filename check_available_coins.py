#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""양측 거래소에 공통으로 상장된 인기 코인 확인"""

import ccxt
import sys
import io

# Windows 콘솔 UTF-8 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 거래소 초기화
binance = ccxt.binance({'enableRateLimit': True})
upbit = ccxt.upbit({'enableRateLimit': True})

print("마켓 정보 로딩 중...")
binance.load_markets()
upbit.load_markets()

# 바이낸스 USDT 마켓 코인
binance_coins = set()
for symbol in binance.markets:
    if '/USDT' in symbol:
        coin = symbol.split('/')[0]
        binance_coins.add(coin)

# 업비트 KRW 마켓 코인
upbit_coins = set()
for symbol in upbit.markets:
    if '/KRW' in symbol:
        coin = symbol.split('/')[0]
        upbit_coins.add(coin)

# 공통 코인
common_coins = binance_coins & upbit_coins

print(f"\n바이낸스 USDT 마켓: {len(binance_coins)}개")
print(f"업비트 KRW 마켓: {len(upbit_coins)}개")
print(f"공통 코인: {len(common_coins)}개\n")

# 인기 알트코인 리스트 (시가총액 기준)
popular_alts = [
    'SOL', 'ADA', 'DOGE', 'AVAX', 'DOT', 'MATIC', 'LINK', 'UNI',
    'ATOM', 'LTC', 'BCH', 'ETC', 'XLM', 'ALGO', 'VET',
    'SAND', 'MANA', 'AXS', 'CHZ', 'ENJ', 'THETA'
]

print("=" * 80)
print("양측 거래소에 모두 상장된 인기 알트코인:")
print("=" * 80)

available_alts = []
for coin in popular_alts:
    if coin in common_coins:
        available_alts.append(coin)
        print(f"✓ {coin:10s} - {coin}/USDT (바이낸스) & {coin}/KRW (업비트)")

print(f"\n총 {len(available_alts)}개 코인 사용 가능")
