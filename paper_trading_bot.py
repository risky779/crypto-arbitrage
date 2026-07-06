#!/usr/bin/env python3
import ccxt, os, sys, io, time, json
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# ========== 페이퍼 트레이딩 설정 ==========
PAPER_MODE = True  # 실거래 금지
COIN = 'DOGE/KRW'
INITIAL_CAPITAL = 44000

# 그리드 전략 (옵션2: 균형)
GRID_CAPITAL = 33000  # 75%
GRID_LEVELS = 3  # 레벨당 11,000원
GRID_RANGE_PERCENT = 2.5  # ±2.5%
PROFIT_PER_GRID = 0.012  # 1.2%

# 브레이크아웃 전략
BREAKOUT_CAPITAL = 11000  # 25%
DROP_THRESHOLD = -2.5  # 더 빨리 진입
TARGET_PROFIT = 2.0
STOP_LOSS = -5.0

FEE_RATE = 0.0005
MIN_ORDER_KRW = 5000
CHECK_INTERVAL = 60  # 1분

# 로그 파일
LOG_FILE = 'paper_trading_log.json'
SUMMARY_FILE = 'paper_trading_summary.txt'

print("=" * 80)
print("📝 페이퍼 트레이딩 봇 (모의 거래)")
print("=" * 80)
print(f"⚠️  실거래 모드: {'OFF' if PAPER_MODE else 'ON'} (안전)")
print(f"💰 가상 자금: {INITIAL_CAPITAL:,}원")
print(f"📊 코인: {COIN}")
print(f"🔢 그리드: {GRID_LEVELS}레벨, ±{GRID_RANGE_PERCENT}%")
print(f"🎢 브레이크아웃: {DROP_THRESHOLD}% 급락 감지")
print(f"📁 로그: {LOG_FILE}")
print("=" * 80)

# 업비트 연결 (가격 조회만)
upbit = ccxt.upbit({'enableRateLimit': True})

# 초기 가격
ticker = upbit.fetch_ticker(COIN)
current_price = ticker['last']
print(f"\n✅ 시작 가격: {current_price:,.2f}원")

# 그리드 레벨 설정
grid_center = current_price
grid_bottom = grid_center * (1 - GRID_RANGE_PERCENT / 100)
grid_top = grid_center * (1 + GRID_RANGE_PERCENT / 100)
grid_step = (grid_top - grid_bottom) / (GRID_LEVELS - 1)
grid_levels = [grid_bottom + i * grid_step for i in range(GRID_LEVELS)]

print(f"\n📊 그리드 레벨:")
for i, level in enumerate(grid_levels):
    print(f"  L{i+1}: {level:,.2f}원")

print(f"\n🚀 페이퍼 트레이딩 시작 (Ctrl+C 중지)")
print("=" * 80)

# 상태 변수
krw = INITIAL_CAPITAL
coin = 0
grid_positions = {i: {'buy_price': None, 'amount': 0} for i in range(GRID_LEVELS)}
breakout_position = None
trades = []
price_history = []
start_time = datetime.now()
start_capital = INITIAL_CAPITAL

# 기존 로그 로드
try:
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        trades = json.load(f)
except:
    trades = []

iteration = 0
previous_price = None

try:
    while True:
        iteration += 1
        now = datetime.now()
        elapsed = (now - start_time).total_seconds() / 60

        # 현재가 조회
        try:
            ticker = upbit.fetch_ticker(COIN)
            current_price = ticker['last']
        except Exception as e:
            print(f"[{now.strftime('%H:%M:%S')}] ⚠️ 가격 조회 실패: {e}")
            time.sleep(CHECK_INTERVAL)
            continue

        # 가격 히스토리
        price_history.append(current_price)
        if len(price_history) > 30:
            price_history.pop(0)

        # 포트폴리오 가치
        portfolio_value = krw + (coin * current_price)
        profit = portfolio_value - start_capital
        profit_pct = (profit / start_capital) * 100

        # 주기적 출력 (5분마다)
        if iteration % 5 == 1:
            print(f"\n[{now.strftime('%m/%d %H:%M:%S')}] 체크 #{iteration} (경과 {elapsed:.0f}분)")
            print(f"  가격: {current_price:,.2f}원")
            print(f"  포트폴리오: {portfolio_value:,.0f}원 (KRW: {krw:,.0f} + DOGE: {coin:.2f}개)")
            print(f"  수익: {profit:+,.0f}원 ({profit_pct:+.2f}%) | 거래: {len([t for t in trades if 'profit' in t or t['type'] == 'BUY'])}회")

        # ========== 브레이크아웃 로직 ==========
        if len(price_history) >= 5:
            recent_high = max(price_history[-5:])
            drop_pct = ((current_price - recent_high) / recent_high) * 100

            # 진입
            if breakout_position is None and drop_pct <= DROP_THRESHOLD:
                available = krw - (GRID_CAPITAL - sum([grid_positions[i]['buy_price'] * grid_positions[i]['amount'] if grid_positions[i]['buy_price'] else 0 for i in range(GRID_LEVELS)]))

                if available >= MIN_ORDER_KRW:
                    buy_price = current_price * 1.0002
                    buy_amount = available / buy_price
                    fee = buy_price * buy_amount * FEE_RATE

                    krw -= (buy_price * buy_amount + fee)
                    coin += buy_amount

                    breakout_position = {
                        'entry_price': buy_price,
                        'amount': buy_amount,
                        'time': now.isoformat()
                    }

                    trade = {
                        'time': now.isoformat(),
                        'strategy': 'BREAKOUT',
                        'type': 'BUY',
                        'price': buy_price,
                        'amount': buy_amount,
                        'drop': drop_pct,
                        'portfolio_value': portfolio_value
                    }
                    trades.append(trade)

                    print(f"\n  🎢 브레이크아웃 진입!")
                    print(f"    급락: {drop_pct:.2f}%")
                    print(f"    매수: {buy_amount:.2f}개 @ {buy_price:,.2f}원")

            # 청산
            elif breakout_position is not None:
                entry_price = breakout_position['entry_price']
                target_price = entry_price * (1 + TARGET_PROFIT / 100)
                stop_price = entry_price * (1 + STOP_LOSS / 100)
                current_pnl = ((current_price - entry_price) / entry_price) * 100

                if current_price >= target_price:
                    sell_price = current_price * 0.9998
                    sell_amount = breakout_position['amount']
                    fee = sell_price * sell_amount * FEE_RATE
                    krw_received = sell_price * sell_amount - fee

                    krw += krw_received
                    coin -= sell_amount

                    profit_trade = krw_received - (entry_price * sell_amount)

                    trade = {
                        'time': now.isoformat(),
                        'strategy': 'BREAKOUT',
                        'type': 'SELL_PROFIT',
                        'price': sell_price,
                        'amount': sell_amount,
                        'profit': profit_trade,
                        'portfolio_value': portfolio_value
                    }
                    trades.append(trade)

                    print(f"\n  ✅ 브레이크아웃 청산 (수익)")
                    print(f"    매도: {sell_amount:.2f}개 @ {sell_price:,.2f}원")
                    print(f"    수익: {profit_trade:+,.0f}원")

                    breakout_position = None

                elif current_price <= stop_price:
                    sell_price = current_price * 0.9998
                    sell_amount = breakout_position['amount']
                    fee = sell_price * sell_amount * FEE_RATE
                    krw_received = sell_price * sell_amount - fee

                    krw += krw_received
                    coin -= sell_amount

                    profit_trade = krw_received - (entry_price * sell_amount)

                    trade = {
                        'time': now.isoformat(),
                        'strategy': 'BREAKOUT',
                        'type': 'SELL_LOSS',
                        'price': sell_price,
                        'amount': sell_amount,
                        'profit': profit_trade,
                        'portfolio_value': portfolio_value
                    }
                    trades.append(trade)

                    print(f"\n  ❌ 브레이크아웃 손절")
                    print(f"    매도: {sell_amount:.2f}개 @ {sell_price:,.2f}원")
                    print(f"    손실: {profit_trade:+,.0f}원")

                    breakout_position = None

        # ========== 그리드 로직 ==========
        for level_idx, level_price in enumerate(grid_levels):
            position = grid_positions[level_idx]

            # 매수: 이전 가격이 레벨 위에 있다가 현재 가격이 레벨 이하로 내려왔을 때만
            if position['buy_price'] is None and previous_price is not None \
                    and previous_price > level_price and current_price <= level_price:
                capital_per_level = GRID_CAPITAL / GRID_LEVELS

                if krw >= MIN_ORDER_KRW:
                    buy_amount_krw = min(capital_per_level, krw - 1000)

                    if buy_amount_krw >= MIN_ORDER_KRW:
                        buy_price = current_price * 1.0002
                        buy_amount = buy_amount_krw / buy_price
                        fee = buy_price * buy_amount * FEE_RATE

                        krw -= (buy_price * buy_amount + fee)
                        coin += buy_amount

                        position['buy_price'] = buy_price
                        position['amount'] = buy_amount

                        trade = {
                            'time': now.isoformat(),
                            'strategy': 'GRID',
                            'type': 'BUY',
                            'level': level_idx + 1,
                            'price': buy_price,
                            'amount': buy_amount,
                            'portfolio_value': portfolio_value
                        }
                        trades.append(trade)

                        print(f"  📊 그리드 매수 L{level_idx+1}: {buy_amount:.2f}개 @ {buy_price:,.2f}원")

            # 매도
            elif position['buy_price'] is not None:
                target_price = position['buy_price'] * (1 + PROFIT_PER_GRID)

                if current_price >= target_price:
                    sell_price = current_price * 0.9998
                    sell_amount = position['amount']
                    fee = sell_price * sell_amount * FEE_RATE
                    krw_received = sell_price * sell_amount - fee

                    krw += krw_received
                    coin -= sell_amount

                    profit_trade = krw_received - (position['buy_price'] * sell_amount)

                    trade = {
                        'time': now.isoformat(),
                        'strategy': 'GRID',
                        'type': 'SELL',
                        'level': level_idx + 1,
                        'price': sell_price,
                        'amount': sell_amount,
                        'profit': profit_trade,
                        'portfolio_value': portfolio_value
                    }
                    trades.append(trade)

                    print(f"  📊 그리드 매도 L{level_idx+1}: {sell_amount:.2f}개 @ {sell_price:,.2f}원 → +{profit_trade:,.0f}원")

                    position['buy_price'] = None
                    position['amount'] = 0

        # 로그 저장 (10분마다)
        if iteration % 10 == 0:
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(trades, f, ensure_ascii=False, indent=2)

            # 요약 저장
            grid_trades = [t for t in trades if t['strategy'] == 'GRID' and t['type'] == 'SELL']
            breakout_trades = [t for t in trades if t['strategy'] == 'BREAKOUT' and 'profit' in t]
            grid_profit = sum([t.get('profit', 0) for t in grid_trades])
            breakout_profit = sum([t.get('profit', 0) for t in breakout_trades])

            summary = f"""
페이퍼 트레이딩 요약
{'='*60}
시작: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
현재: {now.strftime('%Y-%m-%d %H:%M:%S')}
경과: {elapsed:.0f}분

초기 자금: {start_capital:,}원
현재 가치: {portfolio_value:,.0f}원
순수익: {profit:+,.0f}원 ({profit_pct:+.2f}%)

그리드 거래: {len(grid_trades)}회 → {grid_profit:+,.0f}원
브레이크아웃: {len(breakout_trades)}회 → {breakout_profit:+,.0f}원

현재 보유:
  KRW: {krw:,.0f}원
  DOGE: {coin:.2f}개 (≈{coin * current_price:,.0f}원)
"""
            with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
                f.write(summary)

        previous_price = current_price
        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n\n⏸️ 페이퍼 트레이딩 중지")

# 최종 결과
print("\n" + "=" * 80)
print("📊 최종 결과")
print("=" * 80)

final_value = krw + (coin * current_price)
final_profit = final_value - start_capital
final_profit_pct = (final_profit / start_capital) * 100

grid_trades = [t for t in trades if t['strategy'] == 'GRID' and t['type'] == 'SELL']
breakout_trades = [t for t in trades if t['strategy'] == 'BREAKOUT' and 'profit' in t]
grid_profit = sum([t.get('profit', 0) for t in grid_trades])
breakout_profit = sum([t.get('profit', 0) for t in breakout_trades])

print(f"\n기간: {start_time.strftime('%m/%d %H:%M')} ~ {datetime.now().strftime('%m/%d %H:%M')}")
print(f"경과: {elapsed:.0f}분 ({elapsed/60:.1f}시간)")

print(f"\n💰 수익:")
print(f"  초기: {start_capital:,}원")
print(f"  최종: {final_value:,.0f}원")
print(f"  순수익: {final_profit:+,.0f}원 ({final_profit_pct:+.2f}%)")

print(f"\n📊 거래:")
print(f"  그리드: {len(grid_trades)}회 → {grid_profit:+,.0f}원")
print(f"  브레이크아웃: {len(breakout_trades)}회 → {breakout_profit:+,.0f}원")

print(f"\n💼 최종 보유:")
print(f"  KRW: {krw:,.0f}원")
print(f"  DOGE: {coin:.2f}개 (≈{coin * current_price:,.0f}원)")

print(f"\n📁 로그 저장: {LOG_FILE}")
print("=" * 80)
