#!/usr/bin/env python3
import ccxt, os, sys, io, time
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'enableRateLimit': True})
okx = ccxt.okx({'enableRateLimit': True})

COINS = ['XRP', 'XLM', 'ALGO', 'ID', 'BAT', 'MMT', 'DOGE', 'ADA', 'DOT', 'LINK']
RATE = 1480
TARGET_SPREAD = 0.6  # 목표 차익률
LOG_FILE = 'spread_data.log'

print("=== 차익 모니터링 시작 ===\n", flush=True)
print(f"코인: {', '.join(COINS)}", flush=True)
print(f"목표 차익: {TARGET_SPREAD}% 이상", flush=True)
print(f"로그: {LOG_FILE}\n", flush=True)
print("Ctrl+C로 중지\n", flush=True)
print("-" * 80, flush=True)

opportunity_count = 0
last_opportunity = {}  # 코인별 마지막 기회 추적

with open(LOG_FILE, 'a', encoding='utf-8') as log:
    log.write(f"\n\n=== 모니터링 시작: {datetime.now()} ===\n")

    try:
        while True:
            timestamp = datetime.now().strftime('%H:%M:%S')

            for coin in COINS:
                try:
                    # 가격 조회
                    okx_ticker = okx.fetch_ticker(f'{coin}/USDT')
                    upbit_ticker = upbit.fetch_ticker(f'{coin}/KRW')

                    okx_price = okx_ticker['last']
                    upbit_price = upbit_ticker['last']
                    okx_krw = okx_price * RATE

                    # 차익률 계산 (수수료 0.4% 차감)
                    spread_pct = ((upbit_price - okx_krw) / okx_krw) * 100 - 0.4

                    # 화면 출력 (간략)
                    status = "✅" if spread_pct >= TARGET_SPREAD else "  "
                    print(f"{status} [{timestamp}] {coin:6s} | OKX: {okx_krw:7.2f}원 | 업비트: {upbit_price:7.2f}원 | 차익: {spread_pct:+5.2f}%", flush=True)

                    # 로그 기록 (모든 데이터)
                    log.write(f"{timestamp},{coin},{okx_price:.6f},{upbit_price:.2f},{spread_pct:.4f}\n")
                    log.flush()

                    # 0.6% 이상 차익 발견
                    if spread_pct >= TARGET_SPREAD:
                        opportunity_count += 1

                        # 새로운 기회인지 확인
                        if coin not in last_opportunity:
                            alert_msg = f"\n{'='*80}\n🎯 차익 기회 #{opportunity_count}: {coin} {spread_pct:.2f}%\n   OKX: ${okx_price:.6f} ({okx_krw:.2f}원) | 업비트: {upbit_price:.2f}원\n   시작: {timestamp}\n{'='*80}\n"
                            print(alert_msg, flush=True)
                            log.write(alert_msg)
                            log.flush()

                            last_opportunity[coin] = {
                                'start_time': timestamp,
                                'max_spread': spread_pct,
                                'count': 1
                            }
                        else:
                            # 기존 기회 지속
                            last_opportunity[coin]['count'] += 1
                            if spread_pct > last_opportunity[coin]['max_spread']:
                                last_opportunity[coin]['max_spread'] = spread_pct

                    # 기회 종료 감지
                    elif coin in last_opportunity:
                        duration = last_opportunity[coin]['count'] * 12  # 12초마다 체크
                        end_msg = f"⏹️  {coin} 기회 종료 | 지속: {duration}초 | 최대 차익: {last_opportunity[coin]['max_spread']:.2f}% | 종료: {timestamp}\n"
                        print(end_msg, flush=True)
                        log.write(end_msg)
                        log.flush()
                        del last_opportunity[coin]

                except Exception as e:
                    print(f"   [{timestamp}] {coin} 오류: {str(e)[:40]}", flush=True)
                    continue

            print("-" * 80, flush=True)
            time.sleep(12)  # 12초마다 체크

    except KeyboardInterrupt:
        print("\n\n=== 모니터링 종료 ===", flush=True)
        log.write(f"\n=== 모니터링 종료: {datetime.now()} ===\n")
        log.write(f"총 차익 기회: {opportunity_count}회\n")

        # 진행 중인 기회 정리
        if last_opportunity:
            print("\n진행 중이던 기회:", flush=True)
            log.write("\n진행 중이던 기회:\n")
            for coin, info in last_opportunity.items():
                duration = info['count'] * 12
                msg = f"  {coin}: {duration}초 지속, 최대 차익 {info['max_spread']:.2f}%\n"
                print(msg, flush=True)
                log.write(msg)

        print(f"\n총 {opportunity_count}회 차익 기회 발견", flush=True)
        print(f"로그 저장: {LOG_FILE}", flush=True)
