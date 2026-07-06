#!/usr/bin/env python3
import ccxt, os, sys, io, time, threading
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# ========== 조합 전략 설정 (테스트) ==========
COIN = 'DOGE/KRW'
TOTAL_CAPITAL = 10000  # 총 자금 (테스트)
GRID_CAPITAL = 6000    # 그리드용 (60%)
BREAKOUT_CAPITAL = 4000  # 브레이크아웃용 (40%)

# 그리드 설정
GRID_LEVELS = 2  # 2레벨 (각 3000원)
GRID_RANGE_PERCENT = 4.0
PROFIT_PER_GRID = 0.012
FEE_RATE = 0.0005
MIN_ORDER_KRW = 5000

# 브레이크아웃 설정
DROP_THRESHOLD = -3.0  # 3% 급락
TARGET_PROFIT = 2.0    # 2% 수익
STOP_LOSS = -5.0       # 5% 손절

CHECK_INTERVAL = 60  # 1분
MAX_RUNTIME_MINUTES = 60  # 1시간 테스트

print("=" * 80)
print("🤝 조합 전략: 그리드 + 브레이크아웃")
print("=" * 80)
print(f"총 자금: {TOTAL_CAPITAL:,}원")
print(f"  그리드: {GRID_CAPITAL:,}원 (안정 수익)")
print(f"  브레이크아웃: {BREAKOUT_CAPITAL:,}원 (기회 포착)")
print("=" * 80)

# 업비트 연결
upbit = ccxt.upbit({
    'apiKey': os.getenv('UPBIT_ACCESS_KEY'),
    'secret': os.getenv('UPBIT_SECRET_KEY'),
    'enableRateLimit': True
})

# 초기 잔고 확인
balance = upbit.fetch_balance()
krw_available = balance['KRW']['free']

if krw_available < TOTAL_CAPITAL:
    print(f"❌ KRW 부족: {krw_available:,.0f}원 < {TOTAL_CAPITAL:,}원")
    sys.exit(1)

print(f"✅ KRW 잔고: {krw_available:,.0f}원")

# 현재가
ticker = upbit.fetch_ticker(COIN)
current_price = ticker['last']
print(f"✅ {COIN} 현재가: {current_price:,.2f}원")

# 그리드 설정
grid_center = current_price
grid_bottom = grid_center * (1 - GRID_RANGE_PERCENT / 100)
grid_top = grid_center * (1 + GRID_RANGE_PERCENT / 100)
grid_step = (grid_top - grid_bottom) / (GRID_LEVELS - 1) if GRID_LEVELS > 1 else 0
grid_levels = [grid_bottom + i * grid_step for i in range(GRID_LEVELS)]
capital_per_level = GRID_CAPITAL / GRID_LEVELS

print(f"\n📊 그리드 설정:")
print(f"  레벨: {GRID_LEVELS}개")
print(f"  범위: {grid_bottom:,.0f}원 ~ {grid_top:,.0f}원")
print(f"  레벨당: {capital_per_level:,.0f}원")

print(f"\n🎢 브레이크아웃 설정:")
print(f"  대기 자금: {BREAKOUT_CAPITAL:,}원")
print(f"  진입: {DROP_THRESHOLD}% 급락")
print(f"  목표: {TARGET_PROFIT}% 수익")
print(f"  손절: {STOP_LOSS}%")

print("\n⏳ 3초 후 시작...")
time.sleep(3)

# 상태 변수
grid_positions = {i: {'buy_price': None, 'amount': 0} for i in range(GRID_LEVELS)}
breakout_position = None
trades = []
grid_krw_used = 0
breakout_krw_used = 0
start_time = datetime.now()
running = True

# 가격 히스토리 (급락 감지용)
price_history = []

print("\n" + "=" * 80)
print("🚀 조합 전략 시작")
print("=" * 80)

try:
    iteration = 0

    while running:
        iteration += 1
        now = datetime.now()
        elapsed = (now - start_time).total_seconds() / 60

        if elapsed >= MAX_RUNTIME_MINUTES:
            print(f"\n⏰ {MAX_RUNTIME_MINUTES}분 도달. 종료.")
            break

        print(f"\n[{now.strftime('%H:%M:%S')}] 체크 #{iteration} (경과: {elapsed:.1f}분)")

        try:
            ticker = upbit.fetch_ticker(COIN)
            current_price = ticker['last']
            balance = upbit.fetch_balance()
            krw_now = balance['KRW']['free']
            coin_now = balance.get('DOGE', {}).get('free', 0)

            print(f"  현재가: {current_price:,.2f}원 | KRW: {krw_now:,.0f}원 | DOGE: {coin_now:.2f}개")

            # 가격 히스토리 업데이트 (최근 30개)
            price_history.append({'time': now, 'price': current_price})
            if len(price_history) > 30:
                price_history.pop(0)

        except Exception as e:
            print(f"  ⚠️ 조회 실패: {e}")
            time.sleep(CHECK_INTERVAL)
            continue

        # ========== 브레이크아웃 로직 ==========

        # 급락 감지 (최근 30분 vs 현재)
        if len(price_history) >= 5:
            recent_high = max([p['price'] for p in price_history[-5:]])
            drop_pct = ((current_price - recent_high) / recent_high) * 100

            # 포지션 없고, 급락 감지
            if breakout_position is None and drop_pct <= DROP_THRESHOLD:
                available_krw = krw_now - GRID_CAPITAL

                if available_krw >= MIN_ORDER_KRW:
                    buy_amount_coin = available_krw / current_price

                    try:
                        order = upbit.create_market_buy_order(COIN, buy_amount_coin)
                        actual_filled = order.get('filled', buy_amount_coin)
                        actual_price = order.get('average', current_price)

                        breakout_position = {
                            'entry_price': actual_price,
                            'amount': actual_filled,
                            'entry_time': now
                        }
                        breakout_krw_used = available_krw

                        trades.append({
                            'time': now,
                            'strategy': 'BREAKOUT',
                            'type': 'BUY',
                            'price': actual_price,
                            'amount': actual_filled,
                            'drop': drop_pct
                        })

                        print(f"\n  🎢 브레이크아웃 진입!")
                        print(f"    급락: {drop_pct:.2f}%")
                        print(f"    🟢 매수: {actual_filled:.2f}개 @ {actual_price:,.2f}원")

                    except Exception as e:
                        print(f"    ❌ 매수 실패: {e}")

            # 포지션 있을 때: 목표/손절 체크
            elif breakout_position is not None:
                entry_price = breakout_position['entry_price']
                target_price = entry_price * (1 + TARGET_PROFIT / 100)
                stop_price = entry_price * (1 + STOP_LOSS / 100)
                current_pnl = ((current_price - entry_price) / entry_price) * 100

                # 목표 도달
                if current_price >= target_price:
                    sell_amount = breakout_position['amount'] * 0.99

                    try:
                        order = upbit.create_market_sell_order(COIN, sell_amount)
                        actual_krw = order.get('cost', sell_amount * current_price)

                        profit = actual_krw - (entry_price * sell_amount)

                        trades.append({
                            'time': now,
                            'strategy': 'BREAKOUT',
                            'type': 'SELL_PROFIT',
                            'price': current_price,
                            'amount': sell_amount,
                            'profit': profit
                        })

                        print(f"\n  🎯 브레이크아웃 청산!")
                        print(f"    🔴 매도: {sell_amount:.2f}개 @ {current_price:,.2f}원")
                        print(f"    ✅ 수익: {profit:+,.0f}원")

                        breakout_position = None
                        breakout_krw_used = 0

                    except Exception as e:
                        print(f"    ❌ 매도 실패: {e}")

                # 손절
                elif current_price <= stop_price:
                    sell_amount = breakout_position['amount'] * 0.99

                    try:
                        order = upbit.create_market_sell_order(COIN, sell_amount)
                        actual_krw = order.get('cost', sell_amount * current_price)

                        profit = actual_krw - (entry_price * sell_amount)

                        trades.append({
                            'time': now,
                            'strategy': 'BREAKOUT',
                            'type': 'SELL_LOSS',
                            'price': current_price,
                            'amount': sell_amount,
                            'profit': profit
                        })

                        print(f"\n  🛑 브레이크아웃 손절!")
                        print(f"    🔴 매도: {sell_amount:.2f}개 @ {current_price:,.2f}원")
                        print(f"    ❌ 손실: {profit:+,.0f}원")

                        breakout_position = None
                        breakout_krw_used = 0

                    except Exception as e:
                        print(f"    ❌ 매도 실패: {e}")

                else:
                    print(f"    📍 브레이크아웃 보유 중: {current_pnl:+.2f}%")

        # ========== 그리드 로직 ==========

        for level_idx, level_price in enumerate(grid_levels):
            position = grid_positions[level_idx]

            # 매수
            if position['buy_price'] is None and current_price <= level_price:
                available_krw = krw_now - breakout_krw_used - 1000

                if available_krw >= MIN_ORDER_KRW and grid_krw_used < GRID_CAPITAL:
                    buy_amount_krw = min(capital_per_level, GRID_CAPITAL - grid_krw_used, available_krw)

                    if buy_amount_krw >= MIN_ORDER_KRW:
                        buy_amount_coin = buy_amount_krw / current_price

                        try:
                            order = upbit.create_market_buy_order(COIN, buy_amount_coin)
                            actual_filled = order.get('filled', buy_amount_coin)
                            actual_price = order.get('average', current_price)

                            position['buy_price'] = actual_price
                            position['amount'] = actual_filled
                            grid_krw_used += buy_amount_krw

                            trades.append({
                                'time': now,
                                'strategy': 'GRID',
                                'type': 'BUY',
                                'level': level_idx + 1,
                                'price': actual_price,
                                'amount': actual_filled
                            })

                            print(f"  📊 그리드 매수 L{level_idx+1}: {actual_filled:.2f}개 @ {actual_price:,.2f}원")

                        except Exception as e:
                            print(f"  ❌ 그리드 매수 실패 L{level_idx+1}: {e}")

            # 매도
            elif position['buy_price'] is not None:
                target_price = position['buy_price'] * (1 + PROFIT_PER_GRID)

                if current_price >= target_price:
                    sell_amount = position['amount'] * 0.99

                    if sell_amount * current_price >= MIN_ORDER_KRW:
                        try:
                            order = upbit.create_market_sell_order(COIN, sell_amount)
                            actual_krw = order.get('cost', sell_amount * current_price)

                            profit = actual_krw - (position['buy_price'] * sell_amount)

                            trades.append({
                                'time': now,
                                'strategy': 'GRID',
                                'type': 'SELL',
                                'level': level_idx + 1,
                                'price': current_price,
                                'amount': sell_amount,
                                'profit': profit
                            })

                            print(f"  📊 그리드 매도 L{level_idx+1}: {sell_amount:.2f}개 @ {current_price:,.2f}원 → +{profit:,.0f}원")

                            grid_krw_used -= position['buy_price'] * position['amount']
                            position['buy_price'] = None
                            position['amount'] = 0

                        except Exception as e:
                            print(f"  ❌ 그리드 매도 실패 L{level_idx+1}: {e}")

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n\n⏸️  사용자 중지")

# 최종 결과
print("\n" + "=" * 80)
print("📊 최종 결과")
print("=" * 80)

final_balance = upbit.fetch_balance()
final_krw = final_balance['KRW']['free']
final_coin = final_balance.get('DOGE', {}).get('free', 0)
final_price = upbit.fetch_ticker(COIN)['last']

total_value = final_krw + (final_coin * final_price)
net_profit = total_value - (krw_available - (krw_available - TOTAL_CAPITAL))

grid_trades = [t for t in trades if t['strategy'] == 'GRID' and t['type'] == 'SELL']
breakout_trades = [t for t in trades if t['strategy'] == 'BREAKOUT' and 'profit' in t]

grid_profit = sum([t.get('profit', 0) for t in grid_trades])
breakout_profit = sum([t.get('profit', 0) for t in breakout_trades])

print(f"\n💰 수익:")
print(f"  그리드: {grid_profit:+,.0f}원 ({len(grid_trades)}회 거래)")
print(f"  브레이크아웃: {breakout_profit:+,.0f}원 ({len(breakout_trades)}회 거래)")
print(f"  합계: {grid_profit + breakout_profit:+,.0f}원")

print(f"\n💼 잔고:")
print(f"  KRW: {final_krw:,.0f}원")
print(f"  DOGE: {final_coin:.2f}개 (≈{final_coin * final_price:,.0f}원)")
print(f"  총 가치: {total_value:,.0f}원")

print(f"\n⏱️  실행: {elapsed:.1f}분")
print("=" * 80)
