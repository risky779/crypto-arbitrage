#!/usr/bin/env python3
import ccxt, os, sys, io
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

print("=" * 80)
print("🌙 여러 코인 24시간 시뮬레이션")
print("=" * 80)

# 테스트할 코인들
COINS = ['DOGE/KRW', 'SHIB/KRW', 'XRP/KRW', 'XLM/KRW', 'ADA/KRW']
INITIAL_CAPITAL = 44000

# 전략 설정
GRID_CAPITAL_RATIO = 0.7  # 70% 그리드
GRID_LEVELS = 3
GRID_RANGE_PERCENT = 3.0  # ±3%
PROFIT_PER_GRID = 0.012   # 1.2%
DROP_THRESHOLD = -3.0     # 3% 급락
TARGET_PROFIT = 2.0       # 2% 수익
STOP_LOSS = -5.0          # 5% 손절
FEE_RATE = 0.0005
MIN_ORDER_KRW = 5000

print(f"초기 자금: {INITIAL_CAPITAL:,}원")
print(f"테스트 코인: {', '.join([c.split('/')[0] for c in COINS])}")
print(f"기간: 최근 24시간")
print("=" * 80)

upbit = ccxt.upbit({'enableRateLimit': True})

results = []

for coin in COINS:
    print(f"\n{'='*80}")
    print(f"📊 {coin} 분석 중...")
    print(f"{'='*80}")

    try:
        # 1시간봉 데이터 (24시간 = 24개)
        ohlcv = upbit.fetch_ohlcv(coin, '1h', limit=24)

        if not ohlcv or len(ohlcv) < 10:
            print(f"  ❌ 데이터 부족")
            continue

        print(f"  데이터: {len(ohlcv)}개 캔들")
        print(f"  기간: {datetime.fromtimestamp(ohlcv[0][0]/1000).strftime('%m/%d %H:%M')} ~ {datetime.fromtimestamp(ohlcv[-1][0]/1000).strftime('%m/%d %H:%M')}")

        # 가격 통계
        prices = [x[4] for x in ohlcv]
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        volatility = ((max_price - min_price) / avg_price) * 100

        print(f"  평균가: {avg_price:,.2f}원")
        print(f"  변동성: {volatility:.2f}%")

        # 그리드 설정
        start_price = ohlcv[0][4]
        grid_center = start_price
        grid_bottom = grid_center * (1 - GRID_RANGE_PERCENT / 100)
        grid_top = grid_center * (1 + GRID_RANGE_PERCENT / 100)
        grid_step = (grid_top - grid_bottom) / (GRID_LEVELS - 1)
        grid_levels = [grid_bottom + i * grid_step for i in range(GRID_LEVELS)]

        grid_capital = INITIAL_CAPITAL * GRID_CAPITAL_RATIO
        breakout_capital = INITIAL_CAPITAL * (1 - GRID_CAPITAL_RATIO)
        capital_per_level = grid_capital / GRID_LEVELS

        # 시뮬레이션 변수
        krw = INITIAL_CAPITAL
        coin_held = 0
        grid_positions = {i: {'buy_price': None, 'amount': 0} for i in range(GRID_LEVELS)}
        breakout_position = None

        trades = []
        grid_krw_used = 0

        # 가격 히스토리 (급락 감지용)
        price_history = []

        # 시뮬레이션
        for idx, candle in enumerate(ohlcv):
            timestamp = datetime.fromtimestamp(candle[0] / 1000)
            high = candle[2]
            low = candle[3]
            close = candle[4]

            price_history.append(close)
            if len(price_history) > 5:
                price_history.pop(0)

            # 브레이크아웃: 급락 감지
            if len(price_history) >= 3 and breakout_position is None:
                recent_high = max(price_history[:-1])
                drop_pct = ((close - recent_high) / recent_high) * 100

                if drop_pct <= DROP_THRESHOLD:
                    available = krw - grid_krw_used
                    if available >= MIN_ORDER_KRW:
                        buy_price = close * 1.0002
                        buy_amount = available / buy_price
                        fee = buy_price * buy_amount * FEE_RATE

                        krw -= (buy_price * buy_amount + fee)
                        coin_held += buy_amount

                        breakout_position = {
                            'entry_price': buy_price,
                            'amount': buy_amount,
                            'time': timestamp
                        }

                        trades.append({
                            'time': timestamp,
                            'strategy': 'BREAKOUT',
                            'type': 'BUY',
                            'price': buy_price,
                            'amount': buy_amount,
                            'drop': drop_pct
                        })

            # 브레이크아웃: 청산
            elif breakout_position is not None:
                entry_price = breakout_position['entry_price']
                target_price = entry_price * (1 + TARGET_PROFIT / 100)
                stop_price = entry_price * (1 + STOP_LOSS / 100)

                if high >= target_price:
                    sell_price = target_price * 0.9998
                    sell_amount = breakout_position['amount']
                    fee = sell_price * sell_amount * FEE_RATE
                    krw_received = sell_price * sell_amount - fee

                    krw += krw_received
                    coin_held -= sell_amount

                    profit = krw_received - (entry_price * sell_amount)

                    trades.append({
                        'time': timestamp,
                        'strategy': 'BREAKOUT',
                        'type': 'SELL_PROFIT',
                        'price': sell_price,
                        'amount': sell_amount,
                        'profit': profit
                    })

                    breakout_position = None

                elif low <= stop_price:
                    sell_price = stop_price * 0.9998
                    sell_amount = breakout_position['amount']
                    fee = sell_price * sell_amount * FEE_RATE
                    krw_received = sell_price * sell_amount - fee

                    krw += krw_received
                    coin_held -= sell_amount

                    profit = krw_received - (entry_price * sell_amount)

                    trades.append({
                        'time': timestamp,
                        'strategy': 'BREAKOUT',
                        'type': 'SELL_LOSS',
                        'price': sell_price,
                        'amount': sell_amount,
                        'profit': profit
                    })

                    breakout_position = None

            # 그리드: 매수
            for level_idx, level_price in enumerate(grid_levels):
                position = grid_positions[level_idx]

                if position['buy_price'] is None and low <= level_price:
                    if grid_krw_used < grid_capital:
                        buy_amount_krw = min(capital_per_level, grid_capital - grid_krw_used)

                        if buy_amount_krw >= MIN_ORDER_KRW:
                            buy_price = level_price * 1.0002
                            buy_amount = buy_amount_krw / buy_price
                            fee = buy_price * buy_amount * FEE_RATE

                            grid_krw_used += buy_amount_krw
                            coin_held += buy_amount

                            position['buy_price'] = buy_price
                            position['amount'] = buy_amount

                            trades.append({
                                'time': timestamp,
                                'strategy': 'GRID',
                                'type': 'BUY',
                                'level': level_idx + 1,
                                'price': buy_price,
                                'amount': buy_amount
                            })

                # 그리드: 매도
                elif position['buy_price'] is not None:
                    target_price = position['buy_price'] * (1 + PROFIT_PER_GRID)

                    if high >= target_price:
                        sell_price = target_price * 0.9998
                        sell_amount = position['amount']
                        fee = sell_price * sell_amount * FEE_RATE
                        krw_received = sell_price * sell_amount - fee

                        coin_held -= sell_amount

                        profit = krw_received - (position['buy_price'] * sell_amount)

                        trades.append({
                            'time': timestamp,
                            'strategy': 'GRID',
                            'type': 'SELL',
                            'level': level_idx + 1,
                            'price': sell_price,
                            'amount': sell_amount,
                            'profit': profit
                        })

                        grid_krw_used -= position['buy_price'] * position['amount']
                        position['buy_price'] = None
                        position['amount'] = 0

        # 최종 정산
        final_price = ohlcv[-1][4]
        if coin_held > 0:
            krw += coin_held * final_price * (1 - FEE_RATE)
            coin_held = 0

        # 통계
        grid_trades = [t for t in trades if t['strategy'] == 'GRID' and t['type'] == 'SELL']
        breakout_trades = [t for t in trades if t['strategy'] == 'BREAKOUT' and 'profit' in t]

        grid_profit = sum([t.get('profit', 0) for t in grid_trades])
        breakout_profit = sum([t.get('profit', 0) for t in breakout_trades])
        total_profit = krw - INITIAL_CAPITAL

        result = {
            'coin': coin,
            'volatility': volatility,
            'total_trades': len(trades),
            'grid_trades': len(grid_trades),
            'breakout_trades': len(breakout_trades),
            'grid_profit': grid_profit,
            'breakout_profit': breakout_profit,
            'total_profit': total_profit,
            'profit_pct': (total_profit / INITIAL_CAPITAL) * 100
        }

        results.append(result)

        print(f"\n  결과:")
        print(f"    변동성: {volatility:.2f}%")
        print(f"    총 거래: {len(trades)}회")
        print(f"    그리드: {len(grid_trades)}회 → {grid_profit:+,.0f}원")
        print(f"    브레이크아웃: {len(breakout_trades)}회 → {breakout_profit:+,.0f}원")
        print(f"    순수익: {total_profit:+,.0f}원 ({result['profit_pct']:+.2f}%)")

        # 주요 거래 내역
        if trades:
            print(f"\n  주요 거래:")
            for trade in trades[:5]:
                time_str = trade['time'].strftime('%m/%d %H:%M')
                if trade['type'] == 'BUY':
                    extra = f"급락: {trade.get('drop', 0):.1f}%" if 'drop' in trade else f"L{trade.get('level', 0)}"
                    print(f"    {time_str} 🟢 {trade['strategy']:12s} 매수 {extra}")
                else:
                    profit_str = f"{trade.get('profit', 0):+,.0f}원" if 'profit' in trade else ""
                    print(f"    {time_str} 🔴 {trade['strategy']:12s} 매도 {profit_str}")

    except Exception as e:
        print(f"  ❌ 오류: {e}")
        continue

# 결과 요약
print("\n" + "=" * 80)
print("📊 종합 결과")
print("=" * 80)

if results:
    results.sort(key=lambda x: x['total_profit'], reverse=True)

    print("\n🏆 수익률 순위:")
    print("-" * 80)
    for i, r in enumerate(results, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"{emoji} {i}. {r['coin']:12s} | {r['total_profit']:+7,.0f}원 ({r['profit_pct']:+5.2f}%) | 변동성 {r['volatility']:5.2f}% | 거래 {r['total_trades']:2d}회")

    best = results[0]
    print(f"\n✅ 최적 코인: {best['coin']}")
    print(f"   예상 수익: {best['total_profit']:+,.0f}원 ({best['profit_pct']:+.2f}%)")
    print(f"   거래 횟수: {best['total_trades']}회 (그리드 {best['grid_trades']}회, 브레이크아웃 {best['breakout_trades']}회)")

    # 전략별 평균
    avg_grid = sum([r['grid_profit'] for r in results]) / len(results)
    avg_breakout = sum([r['breakout_profit'] for r in results]) / len(results)
    avg_total = sum([r['total_profit'] for r in results]) / len(results)

    print(f"\n📈 평균 수익 (코인당):")
    print(f"   그리드: {avg_grid:+,.0f}원")
    print(f"   브레이크아웃: {avg_breakout:+,.0f}원")
    print(f"   합계: {avg_total:+,.0f}원")

else:
    print("⚠️  결과 없음")

print("\n" + "=" * 80)
