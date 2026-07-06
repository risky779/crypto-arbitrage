#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
빗썸 → 업비트 자동 전송 및 매도
"""
import ccxt
import time
import os
import sys
import io
import requests
from dotenv import load_dotenv
from bithumb_api_v2 import BithumbAPIv2
from upbit_auth import generate_upbit_token
from urllib.parse import urlencode

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# 거래소 초기화
upbit = ccxt.upbit({
    'apiKey': os.getenv('UPBIT_ACCESS_KEY'),
    'secret': os.getenv('UPBIT_SECRET_KEY'),
    'enableRateLimit': True,
})

bithumb_api = BithumbAPIv2()

upbit_access_key = os.getenv('UPBIT_ACCESS_KEY')
upbit_secret_key = os.getenv('UPBIT_SECRET_KEY')
upbit_api_url = 'https://api.upbit.com'

def get_upbit_deposit_address(currency):
    """업비트 입금 주소 조회"""
    query_params = {'currency': currency}
    token = generate_upbit_token(upbit_access_key, upbit_secret_key, query_params)
    headers = {'Authorization': f'Bearer {token}'}

    query_string = urlencode(query_params)
    response = requests.get(
        upbit_api_url + f'/v1/deposits/coin_addresses?{query_string}',
        headers=headers
    )

    if response.status_code == 200:
        data_list = response.json()
        if data_list and len(data_list) > 0:
            data = data_list[0]
            return {
                'address': data.get('deposit_address'),
                'tag': data.get('secondary_address')
            }
        else:
            raise Exception(f"입금 주소가 없습니다")
    else:
        raise Exception(f"주소 조회 실패: {response.json()}")

print("=== 빗썸 → 업비트 자동 전송 및 매도 ===\n")

# 1. 빗썸 잔고 확인
print("1. 빗썸 잔고 확인:")
balance = bithumb_api.get_balance()
coins_to_transfer = []

for coin, info in balance.items():
    if coin != 'KRW':
        total = info.get('free', 0)
        if total > 0.0001:  # 먼지 제외
            coins_to_transfer.append((coin, total))
            print(f"  {coin}: {total:.8f}")

if not coins_to_transfer:
    print("전송할 코인이 없습니다.")
    exit(0)

print(f"\n총 {len(coins_to_transfer)}개 코인 전송 예정\n")

# 2. 각 코인별로 전송 및 매도
for coin, amount in coins_to_transfer:
    print(f"{'='*60}")
    print(f"🔄 {coin} 처리 시작 ({amount:.8f})")
    print(f"{'='*60}\n")

    try:
        # 2-1. 업비트 입금 주소 조회
        print(f"1️⃣ 업비트 입금 주소 조회 중...")

        deposit_info = get_upbit_deposit_address(coin)
        address = deposit_info['address']
        tag = deposit_info.get('tag')

        print(f"   주소: {address}")
        if tag:
            print(f"   태그: {tag}")

        # 2-2. 빗썸에서 출금 (수수료 0.5% 차감)
        withdraw_amount = amount * 0.995
        print(f"\n2️⃣ 빗썸에서 출금 중... ({withdraw_amount:.8f} {coin})")

        withdraw_result = bithumb_api.withdraw(
            currency=coin,
            amount=withdraw_amount,
            address=address,
            secondary_address=tag
        )

        print(f"   ✅ 출금 요청 완료!")
        print(f"   출금 ID: {withdraw_result.get('uuid', 'N/A')}")

        # 2-3. 입금 대기 (최대 20분)
        print(f"\n3️⃣ 업비트 입금 대기 중...")
        print(f"   (최대 20분 대기, 10초마다 확인)")

        start_time = time.time()
        max_wait = 1200  # 20분

        while time.time() - start_time < max_wait:
            time.sleep(10)

            # 업비트 잔고 확인
            upbit_balance = upbit.fetch_balance()
            current_amount = upbit_balance.get(coin, {}).get('free', 0)

            elapsed = int(time.time() - start_time)
            print(f"   [{elapsed}초 경과] {coin} 잔고: {current_amount:.8f}", flush=True)

            if current_amount > 0.0001:
                print(f"   ✅ 입금 완료! ({current_amount:.8f} {coin})")

                # 2-4. 업비트에서 즉시 매도
                print(f"\n4️⃣ 업비트에서 매도 중...")
                sell_order = upbit.create_market_sell_order(f'{coin}/KRW', current_amount)

                print(f"   ✅ 매도 완료!")
                print(f"   주문 ID: {sell_order.get('id')}")

                # 체결 대기
                time.sleep(3)

                # 최종 잔고 확인
                final_balance = upbit.fetch_balance()
                krw_gained = final_balance.get('KRW', {}).get('free', 0)
                print(f"   💰 현재 업비트 KRW: {krw_gained:,.0f}원\n")

                break
        else:
            print(f"   ⏱️ 20분 초과 - 수동으로 확인 필요\n")

    except Exception as e:
        print(f"   ❌ 오류 발생: {e}\n")
        continue

print("="*60)
print("✅ 모든 코인 처리 완료!")
print("="*60)

# 최종 잔고 출력
print("\n=== 최종 잔고 ===")
final_upbit = upbit.fetch_balance()
print(f"업비트 KRW: {final_upbit.get('KRW', {}).get('free', 0):,.0f}원")

final_bithumb = bithumb_api.get_balance()
print(f"빗썸 KRW: {final_bithumb.get('KRW', {}).get('free', 0):,.0f}원")
