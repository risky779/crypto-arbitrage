#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
차익거래 전체 사이클 검증 스크립트
각 단계를 독립적으로 테스트 - 실제 소액 거래 포함

[사이클]
STEP 1. 업비트 코인 매도 → KRW 입금 확인
STEP 2. OKX USDT → 코인 매수 확인
STEP 3. OKX → 업비트 코인 전송 확인
STEP 4. KRW → USDT 재충전 경로 안내 (자동화 불가, 수동)

주의: 실제 소액 거래가 발생합니다. 각 단계마다 확인을 요청합니다.
"""

import ccxt, os, sys, io, time, requests
from dotenv import load_dotenv
from upbit_auth import generate_upbit_token
from urllib.parse import urlencode

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# ========== 설정 ==========
TEST_COIN   = 'XRP'     # 테스트 코인 (XRP: 전송 1~3분, 수수료 0.1개)
TEST_AMOUNT = 5         # 테스트 수량 (XRP 5개 ≈ 2,000원)
UPBIT_MIN_KRW = 5000   # 업비트 최소 주문 금액
# ==========================

okx = ccxt.okx({
    'apiKey':   os.getenv('OKX_API_KEY'),
    'secret':   os.getenv('OKX_SECRET_KEY'),
    'password': os.getenv('OKX_PASSPHRASE'),
    'enableRateLimit': True,
})
upbit = ccxt.upbit({
    'apiKey': os.getenv('UPBIT_ACCESS_KEY'),
    'secret': os.getenv('UPBIT_SECRET_KEY'),
    'enableRateLimit': True,
})


def confirm(msg):
    """계속 진행할지 확인"""
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"  계속하려면 Enter, 건너뛰려면 s, 종료는 q: ", end='')
    ans = input().strip().lower()
    if ans == 'q':
        print("테스트 종료")
        sys.exit(0)
    return ans != 's'


def get_upbit_deposit_address(currency, network=None):
    """업비트 입금 주소 조회"""
    access_key = os.getenv('UPBIT_ACCESS_KEY')
    secret_key = os.getenv('UPBIT_SECRET_KEY')

    query_params = {'currency': currency}
    if network:
        query_params['net_type'] = network

    token = generate_upbit_token(access_key, secret_key, query_params)
    headers = {'Authorization': f'Bearer {token}'}
    query_string = urlencode(query_params)

    resp = requests.get(
        f'https://api.upbit.com/v1/deposits/coin_addresses?{query_string}',
        headers=headers
    )
    if resp.status_code != 200:
        raise Exception(f"주소 조회 실패: {resp.json()}")

    data_list = resp.json()
    if not data_list:
        raise Exception("등록된 입금 주소 없음 (업비트에서 먼저 주소 생성 필요)")

    return {
        'address': data_list[0].get('deposit_address'),
        'tag':     data_list[0].get('secondary_address'),
        'network': data_list[0].get('currency'),
    }


def print_balances():
    """현재 잔고 출력"""
    print("\n[현재 잔고]")
    try:
        ob = okx.fetch_balance()
        ub = upbit.fetch_balance()

        okx_usdt = ob.get('USDT', {}).get('free', 0)
        okx_coin = ob.get(TEST_COIN, {}).get('free', 0)
        ub_krw   = ub.get('KRW', {}).get('free', 0)
        ub_coin  = ub.get(TEST_COIN, {}).get('free', 0)

        print(f"  OKX   : USDT {okx_usdt:.2f}  |  {TEST_COIN} {okx_coin:.4f}")
        print(f"  업비트: KRW  {ub_krw:,.0f}원  |  {TEST_COIN} {ub_coin:.4f}")
    except Exception as e:
        print(f"  잔고 조회 실패: {e}")


# ──────────────────────────────────────────────────────────────────────────────
print("=" * 60)
print("  OKX-업비트 차익거래 사이클 검증")
print(f"  테스트 코인: {TEST_COIN} | 수량: {TEST_AMOUNT}개")
print("=" * 60)

print_balances()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1. 업비트 코인 매도 → KRW
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n\n{'━'*60}")
print(f"  STEP 1: 업비트 {TEST_COIN} 매도 → KRW")
print(f"{'━'*60}")

try:
    ticker = upbit.fetch_ticker(f'{TEST_COIN}/KRW')
    upbit_price = ticker['last']
    estimated_krw = TEST_AMOUNT * upbit_price
    print(f"  현재가: {upbit_price:,.0f}원  |  예상 수령: {estimated_krw:,.0f}원")

    ub_balance = upbit.fetch_balance()
    ub_coin_free = ub_balance.get(TEST_COIN, {}).get('free', 0)
    ub_krw_before = ub_balance.get('KRW', {}).get('free', 0)

    print(f"  업비트 보유 {TEST_COIN}: {ub_coin_free:.4f}개")

    if ub_coin_free < TEST_AMOUNT:
        print(f"  ❌ 업비트 {TEST_COIN} 부족 ({ub_coin_free:.4f} < {TEST_AMOUNT})")
        print(f"     → 이 단계는 건너뜁니다 (STEP 3 완료 후 재시도 가능)")
        step1_ok = False
    elif estimated_krw < UPBIT_MIN_KRW:
        print(f"  ❌ 최소 주문 금액 미달 ({estimated_krw:.0f} < {UPBIT_MIN_KRW}원)")
        step1_ok = False
    elif confirm(f"업비트에서 {TEST_COIN} {TEST_AMOUNT}개 시장가 매도합니다 (약 {estimated_krw:,.0f}원)"):
        order = upbit.create_market_sell_order(f'{TEST_COIN}/KRW', TEST_AMOUNT)
        time.sleep(2)

        ub_balance_after = upbit.fetch_balance()
        ub_krw_after = ub_balance_after.get('KRW', {}).get('free', 0)
        krw_received = ub_krw_after - ub_krw_before

        print(f"\n  ✅ 매도 완료!")
        print(f"     주문 ID  : {order.get('id')}")
        print(f"     KRW 수령 : {krw_received:+,.0f}원")
        print(f"     수수료 후: 약 {estimated_krw * 0.9995:,.0f}원 예상")
        step1_ok = True
    else:
        print("  건너뜀")
        step1_ok = False

except Exception as e:
    print(f"  ❌ 오류: {e}")
    step1_ok = False


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2. OKX USDT → 코인 매수
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n\n{'━'*60}")
print(f"  STEP 2: OKX USDT → {TEST_COIN} 매수")
print(f"{'━'*60}")

try:
    ticker_okx = okx.fetch_ticker(f'{TEST_COIN}/USDT')
    okx_price  = ticker_okx['last']
    usdt_needed = TEST_AMOUNT * okx_price
    print(f"  현재가: ${okx_price:.4f}  |  필요 USDT: {usdt_needed:.2f}")

    ob_balance = okx.fetch_balance()
    okx_usdt_free = ob_balance.get('USDT', {}).get('free', 0)
    okx_coin_before = ob_balance.get(TEST_COIN, {}).get('free', 0)
    print(f"  OKX 보유 USDT: {okx_usdt_free:.2f}")

    if okx_usdt_free < usdt_needed:
        print(f"  ❌ OKX USDT 부족 ({okx_usdt_free:.2f} < {usdt_needed:.2f})")
        step2_ok = False
    elif confirm(f"OKX에서 {TEST_COIN} {TEST_AMOUNT}개 시장가 매수합니다 (약 ${usdt_needed:.2f})"):
        order = okx.create_market_buy_order(f'{TEST_COIN}/USDT', TEST_AMOUNT)
        time.sleep(2)

        ob_balance_after = okx.fetch_balance()
        okx_coin_after = ob_balance_after.get(TEST_COIN, {}).get('free', 0)
        coin_received = okx_coin_after - okx_coin_before

        print(f"\n  ✅ 매수 완료!")
        print(f"     주문 ID   : {order.get('id')}")
        print(f"     체결 수량 : {order.get('filled', coin_received):.4f} {TEST_COIN}")
        print(f"     체결 가격 : ${order.get('average', okx_price):.4f}")
        step2_ok = True
    else:
        print("  건너뜀")
        step2_ok = False

except Exception as e:
    print(f"  ❌ 오류: {e}")
    step2_ok = False


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3. OKX → 업비트 코인 전송
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n\n{'━'*60}")
print(f"  STEP 3: OKX → 업비트 {TEST_COIN} 전송")
print(f"{'━'*60}")

try:
    # 업비트 입금 주소 조회
    print(f"  업비트 {TEST_COIN} 입금 주소 조회 중...")
    deposit_info = get_upbit_deposit_address(TEST_COIN)
    address = deposit_info['address']
    tag     = deposit_info['tag']

    print(f"  주소: {address}")
    if tag:
        print(f"  태그: {tag}")

    # OKX 출금 가능 잔고 확인
    ob_balance = okx.fetch_balance()
    okx_coin_free = ob_balance.get(TEST_COIN, {}).get('free', 0)
    print(f"  OKX 보유 {TEST_COIN}: {okx_coin_free:.4f}개")

    # XRP 네트워크 정보 확인
    try:
        networks = okx.fetch_currencies()
        coin_info = networks.get(TEST_COIN, {})
        networks_list = coin_info.get('networks', {})
        if networks_list:
            print(f"  OKX 지원 네트워크: {list(networks_list.keys())}")
    except Exception:
        pass

    if okx_coin_free < TEST_AMOUNT:
        print(f"  ❌ OKX {TEST_COIN} 부족 ({okx_coin_free:.4f} < {TEST_AMOUNT})")
        step3_ok = False
    elif not address:
        print(f"  ❌ 업비트 입금 주소 없음")
        step3_ok = False
    elif confirm(f"OKX에서 업비트로 {TEST_COIN} {TEST_AMOUNT}개 전송합니다\n  → {address[:20]}...  (태그: {tag})"):
        params = {}
        if tag:
            params['tag'] = tag

        # XRP는 네트워크가 'XRP'
        withdrawal = okx.withdraw(
            code=TEST_COIN,
            amount=TEST_AMOUNT,
            address=address,
            tag=tag,
            params={'network': TEST_COIN, **params}
        )

        print(f"\n  ✅ 출금 요청 완료!")
        print(f"     출금 ID: {withdrawal.get('id')}")
        print(f"     상태   : {withdrawal.get('status')}")
        print(f"     예상 도착: 1~3분 (XRP 기준)")

        # 업비트 입금 대기 (최대 10분)
        print(f"\n  업비트 입금 대기 중...")
        ub_coin_before = upbit.fetch_balance().get(TEST_COIN, {}).get('free', 0)
        start = time.time()

        while time.time() - start < 600:
            time.sleep(15)
            ub_coin_now = upbit.fetch_balance().get(TEST_COIN, {}).get('free', 0)
            elapsed = int(time.time() - start)
            print(f"  [{elapsed:3d}초] 업비트 {TEST_COIN}: {ub_coin_now:.4f}개", flush=True)

            if ub_coin_now > ub_coin_before + TEST_AMOUNT * 0.9:
                arrived = ub_coin_now - ub_coin_before
                print(f"\n  ✅ 입금 확인! {arrived:.4f} {TEST_COIN} 도착 ({elapsed}초 소요)")
                step3_ok = True
                break
        else:
            print(f"\n  ⏱️ 10분 경과, 업비트에서 직접 확인 필요")
            step3_ok = False
    else:
        print("  건너뜀")
        step3_ok = False

except Exception as e:
    print(f"  ❌ 오류: {e}")
    step3_ok = False


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4. KRW → USDT 재충전 안내 (자동화 불가)
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n\n{'━'*60}")
print(f"  STEP 4: KRW → OKX USDT 재충전 경로")
print(f"{'━'*60}")
print("""
  ⚠️  이 단계는 한국 규정상 자동화 불가입니다.

  [방법 A] 수동 환전 (가장 일반적)
    1. 업비트 → 본인 은행 계좌로 KRW 출금
    2. 은행에서 USD 외화 환전
    3. OKX에 USD/USDT 입금

  [방법 B] 빗썸/업비트에서 USDT 구매 후 OKX로 전송
    1. 업비트 KRW → USDT/KRW 마켓에서 USDT 매수
    2. USDT를 OKX 입금 주소로 전송 (TRC20 네트워크 권장)
    ⚠️  업비트 → 해외 거래소 USDT 전송 가능 여부 사전 확인 필요

  [방법 C] 실운용 시 자금 배분 최적화
    - 처음부터 OKX에 USDT를 충분히 예치
    - 업비트에 각 코인 재고를 충분히 예치
    - KRW 수익은 주기적으로 수동 출금
    → 단기간은 재충전 없이 운용 가능
""")


# ══════════════════════════════════════════════════════════════════════════════
# 최종 결과
# ══════════════════════════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print(f"  테스트 결과 요약")
print(f"{'='*60}")
print(f"  STEP 1 업비트 매도  : {'✅' if step1_ok else '❌'}")
print(f"  STEP 2 OKX 매수     : {'✅' if step2_ok else '❌'}")
print(f"  STEP 3 OKX→업비트  : {'✅' if step3_ok else '❌'}")
print(f"  STEP 4 KRW→USDT    : ⚠️  수동 처리")
print()
print_balances()
print(f"{'='*60}\n")
