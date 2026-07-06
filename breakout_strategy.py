#!/usr/bin/env python3
import ccxt, os, sys, io
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

print("=" * 80)
print("🎢 변동성 브레이크아웃 전략 시뮬레이션")
print("=" * 80)

# 설정
COIN = 'DOGE/KRW'
INITIAL_CAPITAL = 44434
DROP_THRESHOLD = -3.0  # 3% 급락 감지 (완화)
TARGET_PROFIT = 2.0    # 2% 반등 목표 (현실적)
STOP_LOSS = -5.0       # 5% 추가 하락 손절 (보수적)
FEE_RATE = 0.0005

print(f"코인: {COIN}")
print(f"초기 자금: {INITIAL_CAPITAL:,}원")
print(f"진입 조건: {DROP_THRESHOLD}% 이상 급락")
print(f"수익 목표: {TARGET_PROFIT}%")
print(f"손절: {STOP_LOSS}%")
print("=" * 80)

# 데이터 수집
upbit = ccxt.upbit({'enableRateLimit': True})

print(f"\n{COIN} 데이터 수집 중 (최근 7일, 1시간봉)...")
ohlcv = upbit.fetch_ohlcv(COIN, '1h', limit=168)

print(f"수집 완료: {len(ohlcv)}개 캔들")
print(f"기간: {datetime.fromtimestamp(ohlcv[0][0]/1000)} ~ {datetime.fromtimestamp(ohlcv[-1][0]/1000)}\n")

# 시뮬레이션
krw = INITIAL_CAPITAL
coin = 0
position = None  # {'entry_price': X, 'amount': Y, 'entry_time': Z}
trades = []

print("=" * 80)
print("시뮬레이션 시작")
print("=" * 80)

for i in range(len(ohlcv)):
    candle = ohlcv[i]
    timestamp = datetime.fromtimestamp(candle[0] / 1000)
    open_p = candle[1]
    high = candle[2]
    low = candle[3]
    close = candle[4]

    # 30분 전 가격 (2캔들 전, 1시간봉이므로 실제론 2시간 전)
    if i < 2:
        continue

    prev_candle = ohlcv[i-2]
    prev_high = prev_candle[2]

    # 급락 감지 (현재 저가가 이전 고가 대비 5% 이상 하락)
    drop_pct = ((low - prev_high) / prev_high) * 100

    # 포지션 없을 때: 급락 감지 → 매수
    if position is None and drop_pct <= DROP_THRESHOLD:
        # 전액 매수
        buy_price = low * 1.0002  # 슬리피지
        buy_amount = krw / buy_price
        fee = buy_price * buy_amount * FEE_RATE
        krw_spent = buy_price * buy_amount + fee

        krw = 0
        coin = buy_amount
        position = {
            'entry_price': buy_price,
            'amount': buy_amount,
            'entry_time': timestamp
        }

        trades.append({
            'time': timestamp,
            'type': 'BUY',
            'price': buy_price,
            'amount': buy_amount,
            'drop': drop_pct
        })

        print(f"[{timestamp}] 🔽 급락 감지 {drop_pct:.2f}%")
        print(f"  🟢 전액 매수: {buy_amount:.2f}개 @ {buy_price:,.2f}원 (수수료 {fee:.0f}원)")

    # 포지션 있을 때: 목표가 or 손절가 체크
    elif position is not None:
        entry_price = position['entry_price']
        target_price = entry_price * (1 + TARGET_PROFIT / 100)
        stop_price = entry_price * (1 + STOP_LOSS / 100)

        # 목표 수익 도달
        if high >= target_price:
            sell_price = target_price * 0.9998  # 슬리피지
            sell_amount = position['amount']
            fee = sell_price * sell_amount * FEE_RATE
            krw_received = sell_price * sell_amount - fee

            krw = krw_received
            coin = 0

            profit = krw - INITIAL_CAPITAL
            profit_pct = (profit / INITIAL_CAPITAL) * 100

            trades.append({
                'time': timestamp,
                'type': 'SELL_PROFIT',
                'price': sell_price,
                'amount': sell_amount,
                'profit': profit,
                'profit_pct': profit_pct
            })

            print(f"[{timestamp}] 🎯 목표가 도달")
            print(f"  🔴 전량 매도: {sell_amount:.2f}개 @ {sell_price:,.2f}원")
            print(f"  ✅ 수익: {profit:+,.0f}원 ({profit_pct:+.2f}%)\n")

            position = None

        # 손절
        elif low <= stop_price:
            sell_price = stop_price * 0.9998  # 슬리피지
            sell_amount = position['amount']
            fee = sell_price * sell_amount * FEE_RATE
            krw_received = sell_price * sell_amount - fee

            krw = krw_received
            coin = 0

            profit = krw - INITIAL_CAPITAL
            profit_pct = (profit / INITIAL_CAPITAL) * 100

            trades.append({
                'time': timestamp,
                'type': 'SELL_LOSS',
                'price': sell_price,
                'amount': sell_amount,
                'profit': profit,
                'profit_pct': profit_pct
            })

            print(f"[{timestamp}] 🛑 손절 발동")
            print(f"  🔴 전량 매도: {sell_amount:.2f}개 @ {sell_price:,.2f}원")
            print(f"  ❌ 손실: {profit:+,.0f}원 ({profit_pct:+.2f}%)\n")

            position = None

# 최종 정산
if coin > 0:
    final_price = ohlcv[-1][4]
    sell_price = final_price * 0.9998
    fee = sell_price * coin * FEE_RATE
    krw = sell_price * coin - fee
    print(f"[최종 정산] 잔여 {coin:.2f}개 @ {sell_price:,.2f}원 → {krw:,.0f}원\n")
    coin = 0

print("=" * 80)
print("결과")
print("=" * 80)

# 통계
buy_trades = [t for t in trades if t['type'] == 'BUY']
profit_trades = [t for t in trades if t['type'] == 'SELL_PROFIT']
loss_trades = [t for t in trades if t['type'] == 'SELL_LOSS']

total_profit = sum([t.get('profit', 0) for t in trades if 'profit' in t])
final_capital = krw
net_profit = final_capital - INITIAL_CAPITAL
net_profit_pct = (net_profit / INITIAL_CAPITAL) * 100

print(f"\n💰 수익 결과:")
print(f"  초기: {INITIAL_CAPITAL:,}원")
print(f"  최종: {final_capital:,.0f}원")
print(f"  순수익: {net_profit:+,.0f}원 ({net_profit_pct:+.2f}%)")

print(f"\n📊 거래 통계:")
print(f"  총 진입: {len(buy_trades)}회")
print(f"  수익 청산: {len(profit_trades)}회")
print(f"  손절: {len(loss_trades)}회")
if len(profit_trades) + len(loss_trades) > 0:
    win_rate = len(profit_trades) / (len(profit_trades) + len(loss_trades)) * 100
    print(f"  승률: {win_rate:.1f}%")

if profit_trades:
    avg_profit = sum([t['profit'] for t in profit_trades]) / len(profit_trades)
    print(f"  평균 수익: {avg_profit:+,.0f}원")

if loss_trades:
    avg_loss = sum([t['profit'] for t in loss_trades]) / len(loss_trades)
    print(f"  평균 손실: {avg_loss:+,.0f}원")

# 기간 환산
days = (ohlcv[-1][0] - ohlcv[0][0]) / (1000 * 60 * 60 * 24)
if days > 0:
    daily = net_profit_pct / days
    monthly = daily * 30
    yearly = daily * 365
    print(f"\n📈 수익률 환산:")
    print(f"  일: {daily:+.3f}%")
    print(f"  월: {monthly:+.2f}%")
    print(f"  연: {yearly:+.1f}%")

print("\n거래 내역:")
print("-" * 80)
for trade in trades:
    time_str = trade['time'].strftime('%m/%d %H:%M')
    if trade['type'] == 'BUY':
        print(f"{time_str} 🟢 매수 | {trade['amount']:.2f}개 @ {trade['price']:,.2f}원 | 급락: {trade['drop']:.2f}%")
    else:
        emoji = '✅' if trade['type'] == 'SELL_PROFIT' else '❌'
        action = '수익' if trade['type'] == 'SELL_PROFIT' else '손절'
        print(f"{time_str} 🔴 매도 ({action}) | {trade['amount']:.2f}개 @ {trade['price']:,.2f}원 | {emoji} {trade['profit']:+,.0f}원 ({trade['profit_pct']:+.2f}%)")

print("\n" + "=" * 80)
print("🆚 그리드와 비교:")
print(f"  그리드 7일: +398원 (+0.90%)")
print(f"  브레이크아웃 7일: {net_profit:+,.0f}원 ({net_profit_pct:+.2f}%)")
if net_profit > 398:
    print(f"  ✅ 브레이크아웃이 {net_profit - 398:+,.0f}원 더 수익")
else:
    print(f"  ❌ 그리드가 {398 - net_profit:+,.0f}원 더 수익")
print("=" * 80)
