#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
from collections import defaultdict

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = defaultdict(lambda: {'count': 0, 'pairs': defaultdict(int), 'profits': []})

with open('arbitrage_log.txt', 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if '순이익' not in line:
            continue

        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue

        try:
            coin = parts[1]
            # 새 형식: 거래소 쌍이 명시됨
            if 'Binance' in parts[2] or 'Upbit-Bithumb' in parts[2]:
                pair = parts[2]
                for p in parts[3:]:
                    if '순이익:' in p:
                        profit_str = p.split('순이익:')[1].replace('%', '').strip()
                        profit = float(profit_str)
                        break
            # 구 형식
            else:
                pair = 'Binance-Upbit'
                for p in parts[2:]:
                    if '순이익:' in p:
                        profit_str = p.split('순이익:')[1].replace('%', '').strip()
                        profit = float(profit_str)
                        break

            data[coin]['count'] += 1
            data[coin]['pairs'][pair] += 1
            data[coin]['profits'].append(profit)
        except:
            continue

print('='*100)
print('[3-Exchange Arbitrage Analysis Report]')
print('='*100)
total = sum(d['count'] for d in data.values())
print(f'Total Records: {total:,} opportunities detected')
print('='*100)

# 플러스 수익 기회
profitable_coins = {}
for coin, info in data.items():
    positive = [p for p in info['profits'] if p > 0]
    if positive:
        profitable_coins[coin] = positive

if profitable_coins:
    print('\n*** PROFITABLE OPPORTUNITIES (Net Profit > 0%) ***\n')
    for coin in sorted(profitable_coins.keys(), key=lambda x: -len(profitable_coins[x])):
        profits = profitable_coins[coin]
        print(f'{coin:6s}: {len(profits):6,d} profitable trades | Avg: +{sum(profits)/len(profits):6.2f}% | Max: +{max(profits):6.2f}%')
else:
    print('\n*** NO PROFITABLE OPPORTUNITIES YET ***\n')

print('\n' + '='*100)
print('Detailed Statistics by Coin')
print('='*100)

for coin in sorted(data.keys(), key=lambda x: -data[x]['count']):
    info = data[coin]
    avg = sum(info['profits']) / len(info['profits'])
    min_p = min(info['profits'])
    max_p = max(info['profits'])
    positive_count = len([p for p in info['profits'] if p > 0])
    positive_pct = (positive_count / info['count']) * 100 if info['count'] > 0 else 0

    print(f'\n{coin}')
    print(f'  Total Records: {info["count"]:,} | Profitable: {positive_count:,} ({positive_pct:.1f}%)')
    print(f'  Avg Profit: {avg:>7.2f}% | Min: {min_p:>7.2f}% | Max: {max_p:>7.2f}%')
    print(f'  Exchange Pairs:')

    for pair, count in sorted(info['pairs'].items(), key=lambda x: -x[1]):
        pct = (count / info['count']) * 100
        print(f'    - {pair:22s}: {count:5,d} records ({pct:5.1f}%)')

print('\n' + '='*100)
print('Summary')
print('='*100)
if profitable_coins:
    total_profitable = sum(len(v) for v in profitable_coins.values())
    print(f'Total Profitable Opportunities: {total_profitable:,} ({total_profitable/total*100:.2f}%)')
    print(f'Coins with Profit: {len(profitable_coins)}')
else:
    print('No profitable opportunities found yet. Keep monitoring!')
print('='*100)
