#!/usr/bin/env python3
"""김프 모니터링 테스트 - 1회만 실행"""

from arbitrage_monitor import ArbitrageMonitor

if __name__ == "__main__":
    monitor = ArbitrageMonitor()
    print("가격 조회 중...")
    prices, usd_krw = monitor.get_prices()
    if prices:
        monitor.print_status(prices, usd_krw)
        print("\n테스트 완료!")
    else:
        print("가격 조회 실패")
