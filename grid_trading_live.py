#!/usr/bin/env python3
import ccxt, os, sys, io, time
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# ========== 실전 설정 (1만원 엄수) ==========
COIN = 'DOGE/KRW'
INITIAL_CAPITAL = 10000  # 1만원 고정
GRID_LEVELS = 2  # 2레벨 (5000원씩)
GRID_RANGE_PERCENT = 4.0  # ±4%
PROFIT_PER_GRID = 0.012  # 1.2%
FEE_RATE = 0.0005  # 0.05%
MIN_ORDER_KRW = 5000  # 업비트 최소
STOP_LOSS_PERCENT = -10  # 테스트용 -10% (보수적)
CHECK_INTERVAL = 60  # 1분마다 체크

# 안전 장치
MAX_RUNTIME_MINUTES = 60  # 최대 1시간
DRY_RUN = False  # False = 실거래, True = 테스트

print("=" * 80)
print("🤖 그리드 트레이딩 실전 봇 (1만원 테스트)")
print("=" * 80)
print(f"⚠️  초기 자금: {INITIAL_CAPITAL:,}원 (엄수)")
print(f"📊 코인: {COIN}")
print(f"🔢 그리드 레벨: {GRID_LEVELS}개")
print(f"📏 그리드 범위: ±{GRID_RANGE_PERCENT}%")
print(f"🎯 레벨당 수익: {PROFIT_PER_GRID*100}%")
print(f"🛑 스톱로스: {STOP_LOSS_PERCENT}%")
print(f"⏱️  체크 간격: {CHECK_INTERVAL}초")
print(f"⏳ 최대 실행: {MAX_RUNTIME_MINUTES}분")
print(f"🧪 모드: {'테스트 (실거래 안함)' if DRY_RUN else '실거래 모드'}")
print("=" * 80)

# 업비트 연결
upbit = ccxt.upbit({
    'apiKey': os.getenv('UPBIT_ACCESS_KEY'),
    'secret': os.getenv('UPBIT_SECRET_KEY'),
    'enableRateLimit': True
})

# 초기 잔고 확인
print("\n💰 초기 잔고 확인 중...")
try:
    balance = upbit.fetch_balance()
    krw_available = balance['KRW']['free']

    if krw_available < INITIAL_CAPITAL:
        print(f"❌ KRW 잔고 부족: {krw_available:,.0f}원 < {INITIAL_CAPITAL:,}원")
        sys.exit(1)

    print(f"✅ KRW 잔고: {krw_available:,.0f}원")

    # 사용할 자금 제한
    capital_to_use = INITIAL_CAPITAL
    print(f"📌 사용 자금: {capital_to_use:,}원 (나머지는 보존)")

except Exception as e:
    print(f"❌ 잔고 조회 실패: {e}")
    sys.exit(1)

# 현재가 조회
print(f"\n📈 {COIN} 현재가 조회 중...")
try:
    ticker = upbit.fetch_ticker(COIN)
    current_price = ticker['last']
    print(f"✅ 현재가: {current_price:,.2f}원")
except Exception as e:
    print(f"❌ 가격 조회 실패: {e}")
    sys.exit(1)

# 그리드 레벨 설정
grid_center = current_price
grid_bottom = grid_center * (1 - GRID_RANGE_PERCENT / 100)
grid_top = grid_center * (1 + GRID_RANGE_PERCENT / 100)
grid_step = (grid_top - grid_bottom) / (GRID_LEVELS - 1) if GRID_LEVELS > 1 else 0

grid_levels = [grid_bottom + i * grid_step for i in range(GRID_LEVELS)]
capital_per_level = capital_to_use / GRID_LEVELS

print(f"\n🔧 그리드 설정:")
print(f"  중심가: {grid_center:,.2f}원")
print(f"  하단: {grid_bottom:,.2f}원")
print(f"  상단: {grid_top:,.2f}원")
print(f"  레벨당 자금: {capital_per_level:,.0f}원")
print(f"  스톱로스: {grid_center * (1 + STOP_LOSS_PERCENT / 100):,.2f}원")

for i, level in enumerate(grid_levels):
    print(f"  레벨 {i+1}: {level:,.2f}원")

# 확인
print("\n" + "=" * 80)
print("⚠️  실거래 시작")
print("   - 최대 손실: 약 1,000원 (스톱로스 -10%)")
print("   - 예상 수익: 시간당 50-200원")
print("   - 자동 실행: 1시간 후 종료")
print("=" * 80)
print("\n⏳ 3초 후 시작...")
time.sleep(3)

# 봇 상태 변수
grid_positions = {i: {'buy_price': None, 'amount': 0, 'order_id': None} for i in range(GRID_LEVELS)}
trades = []
krw_used = 0
coin_held = 0
stop_loss_price = grid_center * (1 + STOP_LOSS_PERCENT / 100)
stopped = False
start_time = datetime.now()

print("\n" + "=" * 80)
print("🚀 봇 시작 - Ctrl+C로 중지")
print("=" * 80)

try:
    iteration = 0

    while True:
        iteration += 1
        now = datetime.now()
        elapsed = (now - start_time).total_seconds() / 60

        # 최대 실행 시간 체크
        if elapsed >= MAX_RUNTIME_MINUTES:
            print(f"\n⏰ 최대 실행 시간 {MAX_RUNTIME_MINUTES}분 도달. 종료합니다.")
            break

        print(f"\n[{now.strftime('%H:%M:%S')}] 📊 체크 #{iteration} (경과: {elapsed:.1f}분)")

        # 현재가 조회
        try:
            ticker = upbit.fetch_ticker(COIN)
            current_price = ticker['last']
            print(f"  현재가: {current_price:,.2f}원")

            # 현재 잔고
            balance = upbit.fetch_balance()
            krw_now = balance['KRW']['free']
            coin_now = balance.get('DOGE', {}).get('free', 0)

            print(f"  잔고: KRW {krw_now:,.0f}원 | DOGE {coin_now:.2f}개")

        except Exception as e:
            print(f"  ⚠️ 가격 조회 실패: {e}")
            time.sleep(CHECK_INTERVAL)
            continue

        # 스톱로스 체크
        if current_price <= stop_loss_price and not stopped:
            print(f"\n🛑 스톱로스 발동! {current_price:,.2f}원 ≤ {stop_loss_price:,.2f}원")

            if coin_now > 0:
                # 전량 매도
                try:
                    if not DRY_RUN:
                        order = upbit.create_market_sell_order(COIN, coin_now * 0.99)
                        print(f"  ✅ 손절 매도: {coin_now:.2f}개")
                        trades.append({
                            'time': now,
                            'type': 'STOP_LOSS',
                            'price': current_price,
                            'amount': coin_now
                        })
                    else:
                        print(f"  [테스트] 손절 매도: {coin_now:.2f}개")

                    stopped = True
                    break

                except Exception as e:
                    print(f"  ❌ 손절 실패: {e}")

        if stopped:
            break

        # 각 그리드 레벨 체크
        for level_idx, level_price in enumerate(grid_levels):
            position = grid_positions[level_idx]

            # 매수 체크 (포지션 없고, 가격이 레벨 이하)
            if position['buy_price'] is None and current_price <= level_price:
                # 사용 가능한 KRW 확인
                if krw_now >= MIN_ORDER_KRW and krw_used < capital_to_use:
                    buy_amount_krw = min(capital_per_level, capital_to_use - krw_used, krw_now - 1000)

                    if buy_amount_krw >= MIN_ORDER_KRW:
                        buy_amount_coin = buy_amount_krw / current_price

                        try:
                            if not DRY_RUN:
                                order = upbit.create_market_buy_order(COIN, buy_amount_coin)
                                actual_filled = order.get('filled', buy_amount_coin)
                                actual_price = order.get('average', current_price)

                                position['buy_price'] = actual_price
                                position['amount'] = actual_filled
                                position['order_id'] = order['id']

                                krw_used += buy_amount_krw

                                trades.append({
                                    'time': now,
                                    'type': 'BUY',
                                    'level': level_idx + 1,
                                    'price': actual_price,
                                    'amount': actual_filled,
                                    'krw': buy_amount_krw
                                })

                                print(f"  🟢 매수 L{level_idx+1}: {actual_filled:.2f}개 @ {actual_price:,.2f}원 ({buy_amount_krw:,.0f}원)")
                            else:
                                print(f"  [테스트] 매수 L{level_idx+1}: {buy_amount_coin:.2f}개 @ {current_price:,.2f}원")
                                position['buy_price'] = current_price
                                position['amount'] = buy_amount_coin

                        except Exception as e:
                            print(f"  ❌ 매수 실패 L{level_idx+1}: {e}")

            # 매도 체크 (포지션 있고, 목표가 도달)
            elif position['buy_price'] is not None:
                target_price = position['buy_price'] * (1 + PROFIT_PER_GRID)

                if current_price >= target_price:
                    sell_amount = position['amount'] * 0.99

                    # 최소 주문 금액 체크
                    if sell_amount * current_price >= MIN_ORDER_KRW:
                        try:
                            if not DRY_RUN:
                                order = upbit.create_market_sell_order(COIN, sell_amount)
                                actual_krw = order.get('cost', sell_amount * current_price)

                                profit = actual_krw - (position['buy_price'] * sell_amount)
                                profit_pct = (profit / (position['buy_price'] * sell_amount)) * 100

                                trades.append({
                                    'time': now,
                                    'type': 'SELL',
                                    'level': level_idx + 1,
                                    'price': current_price,
                                    'amount': sell_amount,
                                    'krw': actual_krw,
                                    'profit': profit,
                                    'profit_pct': profit_pct
                                })

                                print(f"  🔴 매도 L{level_idx+1}: {sell_amount:.2f}개 @ {current_price:,.2f}원 → 수익 {profit:,.0f}원 ({profit_pct:+.2f}%)")

                                # 포지션 초기화
                                krw_used -= position['buy_price'] * position['amount']
                                position['buy_price'] = None
                                position['amount'] = 0
                                position['order_id'] = None

                            else:
                                print(f"  [테스트] 매도 L{level_idx+1}: {sell_amount:.2f}개 @ {current_price:,.2f}원")
                                position['buy_price'] = None
                                position['amount'] = 0

                        except Exception as e:
                            print(f"  ❌ 매도 실패 L{level_idx+1}: {e}")

        # 대기
        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n\n⏸️  사용자 중지")

# 최종 정산
print("\n" + "=" * 80)
print("📊 최종 결과")
print("=" * 80)

try:
    final_balance = upbit.fetch_balance()
    final_krw = final_balance['KRW']['free']
    final_coin = final_balance.get('DOGE', {}).get('free', 0)
    final_price = upbit.fetch_ticker(COIN)['last']

    # 잔여 코인 가치
    coin_value = final_coin * final_price
    total_value = final_krw + coin_value

    # 실제 사용한 자금
    actual_used = INITIAL_CAPITAL - (final_krw - (krw_available - INITIAL_CAPITAL))

    net_profit = total_value - (krw_available - (krw_available - INITIAL_CAPITAL) - INITIAL_CAPITAL)
    net_profit_simple = total_value - INITIAL_CAPITAL

    print(f"\n최종 잔고:")
    print(f"  KRW: {final_krw:,.0f}원")
    print(f"  DOGE: {final_coin:.2f}개 (≈{coin_value:,.0f}원)")
    print(f"  총 가치: {total_value:,.0f}원")

    print(f"\n수익 계산:")
    print(f"  초기: {INITIAL_CAPITAL:,}원")
    print(f"  최종: {total_value:,.0f}원")
    print(f"  순수익: {net_profit_simple:+,.0f}원 ({net_profit_simple/INITIAL_CAPITAL*100:+.2f}%)")

    print(f"\n거래 통계:")
    buy_count = len([t for t in trades if t['type'] == 'BUY'])
    sell_count = len([t for t in trades if t['type'] == 'SELL'])
    total_profit = sum([t.get('profit', 0) for t in trades if t['type'] == 'SELL'])

    print(f"  총 거래: {len(trades)}회")
    print(f"  매수: {buy_count}회")
    print(f"  매도: {sell_count}회")
    if sell_count > 0:
        print(f"  거래 수익 합계: {total_profit:+,.0f}원")
        print(f"  거래당 평균: {total_profit/sell_count:+,.0f}원")

    print(f"\n실행 시간: {(datetime.now() - start_time).total_seconds() / 60:.1f}분")

except Exception as e:
    print(f"최종 정산 오류: {e}")

print("\n" + "=" * 80)
print("✅ 봇 종료")
print("=" * 80)
