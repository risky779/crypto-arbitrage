#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단순 봇 - 0.6% 이상, 5회 제한
"""
import ccxt
import time
import os
from dotenv import load_dotenv

load_dotenv()

upbit = ccxt.upbit({
    'apiKey': os.getenv('UPBIT_ACCESS_KEY'),
    'secret': os.getenv('UPBIT_SECRET_KEY'),
    'enableRateLimit': True,
})

okx = ccxt.okx({
    'apiKey': os.getenv('OKX_API_KEY'),
    'secret': os.getenv('OKX_SECRET_KEY'),
    'password': os.getenv('OKX_PASSPHRASE'),
    'enableRateLimit': True,
})

MIN_PROFIT = 0.4
MAX_TRADES = 5
trade_count = 0
total_profit = 0

print("=== 단순 봇 (0.6%, 5회) ===\n")

coins = ['XRP', 'XLM', 'ALGO', 'BCH', 'ID', 'MMT']

while trade_count < MAX_TRADES:
    try:
        usdt_krw = 1480

        for coin in coins:
            try:
                okx_t = okx.fetch_ticker(f'{coin}/USDT')
                upbit_t = upbit.fetch_ticker(f'{coin}/KRW')

                okx_p = okx_t['last']
                upbit_p = upbit_t['last']
                okx_krw = okx_p * usdt_krw

                profit_n = ((upbit_p - okx_krw) / okx_krw) * 100 - 0.15
                profit_r = ((okx_krw - upbit_p) / upbit_p) * 100 - 0.15

                if profit_n >= MIN_PROFIT:
                    print(f"\n{coin} OKX→업비트 {profit_n:.2f}%")

                    okx_bal = okx.fetch_balance()
                    usdt = min(okx_bal['USDT']['free'] * 0.8, 7)

                    if usdt < 1:
                        continue

                    buy = okx.create_market_buy_order(f'{coin}/USDT', usdt / okx_p)
                    qty = buy['filled']
                    time.sleep(0.5)

                    sell = upbit.create_market_sell_order(f'{coin}/KRW', qty * 0.98)
                    profit = sell['cost'] - (usdt * usdt_krw)

                    total_profit += profit
                    trade_count += 1

                    print(f"완료: +{profit:.0f}원 | 누적: {total_profit:.0f}원 ({trade_count}/{MAX_TRADES})")
                    time.sleep(2)
                    break

                elif profit_r >= MIN_PROFIT:
                    print(f"\n{coin} 업비트→OKX {profit_r:.2f}%")

                    upbit_bal = upbit.fetch_balance()
                    krw = min(upbit_bal['KRW']['free'] * 0.8, 10000)

                    if krw < 5000:
                        continue

                    buy = upbit.create_order(f'{coin}/KRW', 'market', 'buy', None, None, {'cost': krw})
                    qty = buy['filled']
                    time.sleep(0.5)

                    sell = okx.create_market_sell_order(f'{coin}/USDT', qty * 0.98)
                    profit = (sell['cost'] * usdt_krw) - krw

                    total_profit += profit
                    trade_count += 1

                    print(f"완료: +{profit:.0f}원 | 누적: {total_profit:.0f}원 ({trade_count}/{MAX_TRADES})")
                    time.sleep(2)
                    break

            except:
                continue

        time.sleep(10)

    except KeyboardInterrupt:
        break

print(f"\n완료: {trade_count}회, {total_profit:.0f}원")
