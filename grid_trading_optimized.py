#!/usr/bin/env python3
import ccxt, os, sys, io, time
from datetime import datetime, timedelta
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# 최적화된 설정
COIN = 'DOGE/KRW'  # 변동성 높은 코인
INITIAL_CAPITAL = 44434  # 현재 업비트 잔고
GRID_LEVELS = 5  # 7 → 5개 (레벨당 자금 증가)
GRID_RANGE_PERCENT = 5.0  # 3% → 5% (범위 확대)
PROFIT_PER_GRID = 0.012  # 0.8% → 1.2% (수익 목표 상향)
FEE_RATE = 0.0005  # 업비트 수수료 0.05%
MIN_ORDER_KRW = 5000  # 최소 주문 금액
SLIPPAGE = 0.0002  # 슬리피지 0.02%
STOP_LOSS_PERCENT = -15  # 스톱로스 -15%

# 백테스트 기간
DAYS = 7

print("=" * 80)
print("그리드 트레이딩 시뮬레이션 (최적화 버전)")
print("=" * 80)
print(f"코인: {COIN}")
print(f"초기 자금: {INITIAL_CAPITAL:,.0f}원")
print(f"그리드 레벨: {GRID_LEVELS}개 (개선: 7→5)")
print(f"그리드 범위: ±{GRID_RANGE_PERCENT}% (개선: 3%→5%)")
print(f"레벨당 수익: {PROFIT_PER_GRID*100}% (개선: 0.8%→1.2%)")
print(f"수수료: {FEE_RATE*100}%")
print(f"슬리피지: {SLIPPAGE*100}%")
print(f"스톱로스: {STOP_LOSS_PERCENT}%")
print(f"백테스트 기간: 최근 {DAYS}일")
print("=" * 80)

# 업비트 연결
upbit = ccxt.upbit({'enableRateLimit': True})

# 과거 데이터 가져오기
print(f"\n{COIN} 가격 데이터 수집 중...")
try:
    # 1시간봉 데이터 (최근 7일 = 168개)
    ohlcv = upbit.fetch_ohlcv(COIN, '1h', limit=168)

    if not ohlcv or len(ohlcv) < 100:
        print("데이터 부족")
        sys.exit(1)

    print(f"  수집 완료: {len(ohlcv)}개 캔들")
    print(f"  기간: {datetime.fromtimestamp(ohlcv[0][0]/1000)} ~ {datetime.fromtimestamp(ohlcv[-1][0]/1000)}")

    # 데이터 통계
    prices = [x[4] for x in ohlcv]  # 종가
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    volatility = ((max_price - min_price) / avg_price) * 100

    print(f"  평균가: {avg_price:,.2f}원")
    print(f"  최저가: {min_price:,.2f}원")
    print(f"  최고가: {max_price:,.2f}원")
    print(f"  변동성: {volatility:.2f}%")

except Exception as e:
    print(f"데이터 수집 실패: {e}")
    sys.exit(1)

# 그리드 설정
current_price = ohlcv[0][4]
grid_center = current_price
grid_bottom = grid_center * (1 - GRID_RANGE_PERCENT / 100)
grid_top = grid_center * (1 + GRID_RANGE_PERCENT / 100)
grid_step = (grid_top - grid_bottom) / (GRID_LEVELS - 1)

grid_levels = [grid_bottom + i * grid_step for i in range(GRID_LEVELS)]

print(f"\n그리드 레벨 설정:")
print(f"  중심가: {grid_center:,.2f}원")
print(f"  하단: {grid_bottom:,.2f}원")
print(f"  상단: {grid_top:,.2f}원")
print(f"  간격: {grid_step:,.2f}원\n")

for i, level in enumerate(grid_levels):
    print(f"  레벨 {i+1}: {level:,.2f}원")

# 시뮬레이션 변수
krw = INITIAL_CAPITAL
coin = 0
entry_price = grid_center
stop_loss_price = entry_price * (1 + STOP_LOSS_PERCENT / 100)

trades = []
grid_positions = {i: {'buy_price': None, 'amount': 0} for i in range(GRID_LEVELS)}

capital_per_level = INITIAL_CAPITAL / GRID_LEVELS
stopped = False

print(f"\n레벨당 자금: {capital_per_level:,.0f}원 (개선: {INITIAL_CAPITAL/7:,.0f}원→{capital_per_level:,.0f}원)")
print(f"스톱로스 가격: {stop_loss_price:,.2f}원\n")

print("=" * 80)
print("시뮬레이션 시작")
print("=" * 80)

# 백테스트 실행
for idx, candle in enumerate(ohlcv):
    timestamp = datetime.fromtimestamp(candle[0] / 1000)
    open_price = candle[1]
    high = candle[2]
    low = candle[3]
    close = candle[4]

    # 스톱로스 체크
    if low <= stop_loss_price and not stopped:
        # 전량 손절
        if coin > 0:
            sell_price = stop_loss_price * (1 - SLIPPAGE)
            fee = sell_price * coin * FEE_RATE
            krw_received = sell_price * coin - fee

            trades.append({
                'time': timestamp,
                'type': 'STOP_LOSS',
                'price': sell_price,
                'amount': coin,
                'krw': krw_received,
                'fee': fee
            })

            print(f"[{timestamp}] 🛑 스톱로스 발동: {coin:.2f}개 @ {sell_price:,.2f}원 → {krw_received:,.0f}원 (수수료 {fee:.0f}원)")

            krw += krw_received
            coin = 0
            stopped = True
        continue

    if stopped:
        continue

    # 각 그리드 레벨 체크
    for level_idx, level_price in enumerate(grid_levels):
        position = grid_positions[level_idx]

        # 매수 체크 (가격이 레벨 아래로 터치)
        if low <= level_price and position['buy_price'] is None:
            if krw >= MIN_ORDER_KRW:
                buy_price = level_price * (1 + SLIPPAGE)
                buy_amount = min(capital_per_level, krw) / buy_price
                fee = buy_price * buy_amount * FEE_RATE
                krw_spent = buy_price * buy_amount + fee

                if krw_spent <= krw:
                    krw -= krw_spent
                    coin += buy_amount
                    position['buy_price'] = buy_price
                    position['amount'] = buy_amount

                    trades.append({
                        'time': timestamp,
                        'type': 'BUY',
                        'level': level_idx + 1,
                        'price': buy_price,
                        'amount': buy_amount,
                        'krw': krw_spent,
                        'fee': fee
                    })

                    if len(trades) <= 30 or len(trades) % 10 == 0:
                        print(f"[{timestamp}] 🟢 매수 L{level_idx+1}: {buy_amount:.2f}개 @ {buy_price:,.2f}원 (수수료 {fee:.0f}원)")

        # 매도 체크 (포지션 있고 목표가 도달)
        elif position['buy_price'] is not None:
            target_sell_price = position['buy_price'] * (1 + PROFIT_PER_GRID)

            if high >= target_sell_price:
                sell_price = target_sell_price * (1 - SLIPPAGE)
                sell_amount = position['amount']
                fee = sell_price * sell_amount * FEE_RATE
                krw_received = sell_price * sell_amount - fee

                # 최소 주문 금액 체크
                if sell_price * sell_amount >= MIN_ORDER_KRW:
                    krw += krw_received
                    coin -= sell_amount

                    profit = krw_received - (position['buy_price'] * sell_amount)
                    profit_pct = (profit / (position['buy_price'] * sell_amount)) * 100

                    trades.append({
                        'time': timestamp,
                        'type': 'SELL',
                        'level': level_idx + 1,
                        'price': sell_price,
                        'amount': sell_amount,
                        'krw': krw_received,
                        'fee': fee,
                        'profit': profit,
                        'profit_pct': profit_pct
                    })

                    if len(trades) <= 30 or len(trades) % 10 == 0:
                        print(f"[{timestamp}] 🔴 매도 L{level_idx+1}: {sell_amount:.2f}개 @ {sell_price:,.2f}원 → 수익 {profit:,.0f}원 ({profit_pct:+.2f}%)")

                    # 포지션 초기화
                    position['buy_price'] = None
                    position['amount'] = 0

# 최종 정산
final_price = ohlcv[-1][4]
if coin > 0:
    sell_price = final_price * (1 - SLIPPAGE)
    fee = sell_price * coin * FEE_RATE
    krw_final = sell_price * coin - fee
    krw += krw_final
    print(f"\n[최종 정산] 잔여 코인 {coin:.2f}개 @ {sell_price:,.2f}원 → {krw_final:,.0f}원")
    coin = 0

print("\n" + "=" * 80)
print("시뮬레이션 결과")
print("=" * 80)

# 거래 통계
buy_trades = [t for t in trades if t['type'] == 'BUY']
sell_trades = [t for t in trades if t['type'] == 'SELL']
profitable_trades = [t for t in sell_trades if 'profit' in t and t['profit'] > 0]

total_profit = sum([t.get('profit', 0) for t in sell_trades])
total_fee = sum([t['fee'] for t in trades])
final_capital = krw
net_profit = final_capital - INITIAL_CAPITAL
net_profit_pct = (net_profit / INITIAL_CAPITAL) * 100

print(f"\n💰 수익 결과:")
print(f"  초기 자금: {INITIAL_CAPITAL:,.0f}원")
print(f"  최종 자금: {final_capital:,.0f}원")
print(f"  순수익: {net_profit:,.0f}원 ({net_profit_pct:+.2f}%)")

print(f"\n📊 거래 통계:")
print(f"  총 거래: {len(trades)}회")
print(f"  매수: {len(buy_trades)}회")
print(f"  매도: {len(sell_trades)}회")
print(f"  수익 거래: {len(profitable_trades)}회")
print(f"  승률: {len(profitable_trades)/len(sell_trades)*100 if sell_trades else 0:.1f}%")

print(f"\n💸 비용 분석:")
print(f"  총 거래 수익: {total_profit:,.0f}원")
print(f"  총 수수료: {total_fee:,.0f}원")
print(f"  수수료 비율: {total_fee/INITIAL_CAPITAL*100:.2f}%")
print(f"  수익 대비 수수료: {total_fee/total_profit*100 if total_profit > 0 else 0:.1f}%")

if sell_trades:
    avg_profit = total_profit / len(sell_trades)
    print(f"  거래당 평균 수익: {avg_profit:,.0f}원")

# 일일 환산
days_simulated = (ohlcv[-1][0] - ohlcv[0][0]) / (1000 * 60 * 60 * 24)
if days_simulated > 0:
    daily_return = net_profit_pct / days_simulated
    monthly_return = daily_return * 30
    yearly_return = daily_return * 365

    print(f"\n📈 수익률 환산:")
    print(f"  일 수익률: {daily_return:+.3f}%")
    print(f"  월 환산: {monthly_return:+.2f}%")
    print(f"  연 환산: {yearly_return:+.1f}%")

print("\n" + "=" * 80)

# 최근 30개 거래 내역
if len(trades) > 0:
    print("\n주요 거래 내역 (최근 30개):")
    print("-" * 80)
    for trade in trades[-30:]:
        time_str = trade['time'].strftime('%m/%d %H:%M')
        type_emoji = '🟢' if trade['type'] == 'BUY' else '🔴' if trade['type'] == 'SELL' else '🛑'

        if trade['type'] == 'SELL' and 'profit' in trade:
            print(f"{time_str} {type_emoji} {trade['type']:4s} L{trade['level']} | {trade['amount']:>7.2f}개 @ {trade['price']:>7,.2f}원 | 수익: {trade['profit']:>+6,.0f}원 ({trade['profit_pct']:>+5.2f}%)")
        else:
            level = f"L{trade['level']}" if 'level' in trade else "ALL"
            print(f"{time_str} {type_emoji} {trade['type']:4s} {level:3s} | {trade['amount']:>7.2f}개 @ {trade['price']:>7,.2f}원")

print("\n" + "=" * 80)

# 개선 효과 요약
print("\n🎯 최적화 효과:")
print(f"  변동성: XRP 7.92% → DOGE {volatility:.2f}%")
print(f"  레벨당 자금: {INITIAL_CAPITAL/7:,.0f}원 → {capital_per_level:,.0f}원 (+{(capital_per_level/(INITIAL_CAPITAL/7)-1)*100:.1f}%)")
print(f"  목표 수익: 0.8% → 1.2% (+50%)")
print("=" * 80)
