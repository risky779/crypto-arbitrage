#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OKX-업비트-빗썸 김프 모니터링 시스템
바이낸스 대신 OKX 사용
"""

import ccxt
import time
import sys
import io
from datetime import datetime
from typing import Dict, Optional

# Windows 콘솔 UTF-8 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class ArbitrageMonitorOKX:
    def __init__(self):
        # 거래소 초기화
        self.okx = ccxt.okx({
            'enableRateLimit': True,
            'rateLimit': 100,
        })
        self.upbit = ccxt.upbit({
            'enableRateLimit': True,
            'rateLimit': 200,
        })
        self.bithumb = ccxt.bithumb({
            'enableRateLimit': True,
            'rateLimit': 200,
        })

        # 모니터링 대상 코인
        self.symbols = {
            'BTC/USDT': 'BTC/KRW',
            'ETH/USDT': 'ETH/KRW',
            'XRP/USDT': 'XRP/KRW',
            'SOL/USDT': 'SOL/KRW',
            'ADA/USDT': 'ADA/KRW',
            'DOGE/USDT': 'DOGE/KRW',
            'AVAX/USDT': 'AVAX/KRW',
            'DOT/USDT': 'DOT/KRW',
            'LINK/USDT': 'LINK/KRW',
            'UNI/USDT': 'UNI/KRW',
            'ATOM/USDT': 'ATOM/KRW',
            'BCH/USDT': 'BCH/KRW',
            'SAND/USDT': 'SAND/KRW',
        }

        # 수수료 설정
        self.okx_fee = 0.1      # OKX 거래 수수료
        self.upbit_fee = 0.05    # 업비트 거래 수수료
        self.bithumb_fee = 0.25  # 빗썸 거래 수수료
        self.withdrawal_fee = 0.1  # 입출금 수수료
        self.total_fee_upbit = self.okx_fee + self.upbit_fee + self.withdrawal_fee
        self.total_fee_bithumb = self.okx_fee + self.bithumb_fee + self.withdrawal_fee

        # 기록
        self.max_premium = {}
        self.opportunity_count = 0
        self.log_file = "arbitrage_log_okx.txt"

    def get_usd_krw_rate(self) -> Optional[float]:
        """실시간 USD/KRW 환율 조회"""
        try:
            ticker = self.upbit.fetch_ticker('USDT/KRW')
            return ticker['last']
        except Exception as e:
            print(f"환율 조회 실패: {e}")
            return 1380

    def get_prices(self) -> Dict:
        """각 거래소의 코인 가격 조회"""
        prices = {}
        usd_krw = self.get_usd_krw_rate()

        for okx_symbol, krw_symbol in self.symbols.items():
            try:
                # OKX 가격 (USDT)
                okx_ticker = self.okx.fetch_ticker(okx_symbol)
                okx_price_usdt = okx_ticker['last']
                okx_price_krw = okx_price_usdt * usd_krw

                time.sleep(0.2)

                # 업비트 가격
                upbit_price_krw = None
                try:
                    upbit_ticker = self.upbit.fetch_ticker(krw_symbol)
                    upbit_price_krw = upbit_ticker['last']
                except:
                    pass

                # 빗썸 가격
                bithumb_price_krw = None
                try:
                    bithumb_ticker = self.bithumb.fetch_ticker(krw_symbol)
                    bithumb_price_krw = bithumb_ticker['last']
                except:
                    pass

                time.sleep(0.2)

                coin_name = okx_symbol.split('/')[0]
                prices[coin_name] = {
                    'okx_usdt': okx_price_usdt,
                    'okx_krw': okx_price_krw,
                    'upbit_krw': upbit_price_krw,
                    'bithumb_krw': bithumb_price_krw,
                    'timestamp': datetime.now()
                }

                # 차익률 계산
                opportunities = []

                # OKX vs 업비트
                if upbit_price_krw:
                    premium = ((upbit_price_krw - okx_price_krw) / okx_price_krw) * 100
                    net_profit = premium - self.total_fee_upbit
                    opportunities.append(('OKX-Upbit', premium, net_profit))

                # OKX vs 빗썸
                if bithumb_price_krw:
                    premium = ((bithumb_price_krw - okx_price_krw) / okx_price_krw) * 100
                    net_profit = premium - self.total_fee_bithumb
                    opportunities.append(('OKX-Bithumb', premium, net_profit))

                # 업비트 vs 빗썸
                if upbit_price_krw and bithumb_price_krw:
                    premium = ((bithumb_price_krw - upbit_price_krw) / upbit_price_krw) * 100
                    net_profit = premium - (self.upbit_fee + self.bithumb_fee)
                    opportunities.append(('Upbit-Bithumb', premium, net_profit))

                prices[coin_name]['opportunities'] = opportunities

            except Exception as e:
                print(f"{okx_symbol} 조회 실패: {e}")

        return prices, usd_krw

    def log_opportunity(self, coin: str, pair: str, premium: float, net_profit: float, prices: Dict):
        """차익 기회 기록"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | ")
                f.write(f"{coin:6s} | {pair:16s} | 김프: {premium:>6.2f}% | 순이익: {net_profit:>6.2f}%")

                if 'OKX' in pair:
                    f.write(f" | OKX: ${prices['okx_usdt']:.2f}")
                if 'Upbit' in pair and prices.get('upbit_krw'):
                    f.write(f" | 업비트: {prices['upbit_krw']:.0f}원")
                if 'Bithumb' in pair and prices.get('bithumb_krw'):
                    f.write(f" | 빗썸: {prices['bithumb_krw']:.0f}원")
                f.write("\n")
        except:
            pass

    def print_status(self, prices: Dict, usd_krw: float):
        """현재 상태 출력"""
        print("\n" + "="*100, flush=True)
        print(f"[3개 거래소 김프 모니터링 - OKX/업비트/빗썸] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
        print(f"환율: 1 USDT = {usd_krw:,.2f} KRW | 누적 기회: {self.opportunity_count}회", flush=True)
        print("="*100, flush=True)

        has_opportunity = False
        all_opportunities = []

        for coin, data in prices.items():
            print(f"\n{coin:6s}", flush=True)
            print(f"  OKX:      ${data['okx_usdt']:>12,.2f} USDT  ({data['okx_krw']:>12,.0f} KRW)", flush=True)
            if data.get('upbit_krw'):
                print(f"  업비트:   {data['upbit_krw']:>12,.0f} KRW", flush=True)
            if data.get('bithumb_krw'):
                print(f"  빗썸:     {data['bithumb_krw']:>12,.0f} KRW", flush=True)

            for pair, premium, net_profit in data.get('opportunities', []):
                marker = "[+]" if net_profit > 0.5 else "[-]" if net_profit < -0.5 else "[ ]"
                print(f"    {marker} {pair:16s}: 김프 {premium:>6.2f}% | 순이익 {net_profit:>6.2f}%", end="", flush=True)

                if abs(net_profit) > 0.7:
                    if net_profit > 0:
                        direction = f"{pair.split('-')[1]} 매수 -> {pair.split('-')[0]} 매도"
                    else:
                        direction = f"{pair.split('-')[0]} 매수 -> {pair.split('-')[1]} 매도"
                    print(f"  !!! 차익 기회 !!! {direction}", end="", flush=True)
                    has_opportunity = True
                    all_opportunities.append((coin, pair, net_profit, direction))
                    self.log_opportunity(coin, pair, premium, net_profit, data)
                print(flush=True)

        print("\n" + "="*100, flush=True)

        if has_opportunity:
            self.opportunity_count += 1
            print("\n" + "!"*100, flush=True)
            print("!!! 차익거래 기회 발견 !!!", flush=True)
            for coin, pair, profit, direction in all_opportunities:
                print(f"  - {coin} [{pair}]: 순이익 {profit:+.2f}% ({direction})", flush=True)
            print("!"*100 + "\n", flush=True)

    def run(self, interval: int = 10):
        """모니터링 시작"""
        print("=" * 100, flush=True)
        print("3개 거래소 김프 모니터링 시작 (OKX / 업비트 / 빗썸)", flush=True)
        print(f"업데이트 주기: {interval}초", flush=True)
        print(f"수수료:", flush=True)
        print(f"  - OKX-업비트:   {self.total_fee_upbit}% (OKX {self.okx_fee}% + 업비트 {self.upbit_fee}% + 입출금 {self.withdrawal_fee}%)", flush=True)
        print(f"  - OKX-빗썸:     {self.total_fee_bithumb}% (OKX {self.okx_fee}% + 빗썸 {self.bithumb_fee}% + 입출금 {self.withdrawal_fee}%)", flush=True)
        print(f"  - 업비트-빗썸:  {self.upbit_fee + self.bithumb_fee}% (업비트 {self.upbit_fee}% + 빗썸 {self.bithumb_fee}%)", flush=True)
        print("=" * 100, flush=True)
        print("\n데이터 조회 중...", flush=True)

        try:
            while True:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 가격 조회 중...", flush=True)
                prices, usd_krw = self.get_prices()
                if prices:
                    self.print_status(prices, usd_krw)
                else:
                    print("가격 조회 실패, 재시도 중...", flush=True)
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n모니터링 종료", flush=True)


if __name__ == "__main__":
    monitor = ArbitrageMonitorOKX()
    monitor.run(interval=10)
