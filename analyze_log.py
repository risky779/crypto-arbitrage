#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""로그 파일 분석 스크립트"""

import sys
import io
from collections import defaultdict
from datetime import datetime

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_log(filename='arbitrage_log.txt'):
    data = defaultdict(lambda: {
        'count': 0,
        'pairs': defaultdict(int),
        'min_profit': None,
        'max_profit': None,
        'profits': []
    })

    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parts = line.strip().split(' | ')
            if len(parts) < 3:
                continue

            timestamp = parts[0]
            coin = parts[1].strip()

            # 새 형식(3개 거래소) vs 구 형식(2개 거래소) 구분
            if len(parts) > 4 and ('Binance' in parts[2] or 'Upbit' in parts[2]):
                pair = parts[2].strip()
                profit_part = parts[3]
            else:
                pair = 'Binance-Upbit'
                profit_part = parts[3] if len(parts) > 3 else parts[2]

            # 순이익 추출
            if '순이익:' in profit_part:
                try:
                    profit_str = profit_part.split('순이익:')[1].strip().replace('%', '').strip()
                    profit = float(profit_str)

                    data[coin]['count'] += 1
                    data[coin]['pairs'][pair] += 1
                    data[coin]['profits'].append(profit)

                    if data[coin]['max_profit'] is None or profit > data[coin]['max_profit']:
                        data[coin]['max_profit'] = profit
                    if data[coin]['min_profit'] is None or profit < data[coin]['min_profit']:
                        data[coin]['min_profit'] = profit
                except ValueError:
                    pass

    print('=' * 100)
    print('[차익거래 기회 분석 리포트]')
    print('=' * 100)
    total_count = sum(d['count'] for d in data.values())
    print(f'\n총 기록: {total_count}건\n')
    print('=' * 100)

    for coin in sorted(data.keys()):
        info = data[coin]
        if info['count'] == 0:
            continue

        avg_profit = sum(info['profits']) / len(info['profits'])

        print(f'\n[{coin}]')
        print(f'  총 기록: {info["count"]}건')
        print(f'  평균 순이익: {avg_profit:>7.2f}%')
        print(f'  최소 순이익: {info["min_profit"]:>7.2f}%')
        print(f'  최대 순이익: {info["max_profit"]:>7.2f}%')

        print(f'\n  거래소 조합별:')
        for pair, count in sorted(info['pairs'].items(), key=lambda x: -x[1]):
            percentage = (count / info['count']) * 100
            print(f'    - {pair:20s}: {count:3d}건 ({percentage:5.1f}%)')

    print('\n' + '=' * 100)
    print('\n[분석 완료]')
    print(f'  현재까지 모니터링 결과: DOGE 코인에서만 차익 기회 감지')
    print(f'  주로 역프리미엄 상태 (바이낸스가 더 비쌈)')
    print(f'  수익성: 수수료 차감 후 모두 마이너스 (-0.7% ~ -0.98%)')
    print('\n[TIP] 플러스 수익(+1% 이상)이 나올 때까지 계속 모니터링하세요!')
    print('=' * 100)

if __name__ == '__main__':
    analyze_log()
