#!/usr/bin/env python3
import ccxt, os, sys, io
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY')})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})

print("=== OKX → 업비트 ID 전송 ===\n", flush=True)

# 1. 현재 잔고
okx_bal = okx.fetch_balance()
okx_id = okx_bal.get('ID', {}).get('free', 0)

upbit_bal = upbit.fetch_balance()
upbit_id = upbit_bal.get('ID', {}).get('free', 0)

print(f"현재 잔고:", flush=True)
print(f"  OKX ID: {okx_id:.2f}개", flush=True)
print(f"  업비트 ID: {upbit_id:.2f}개\n", flush=True)

if okx_id < 10:
    print("❌ OKX ID 부족", flush=True)
    sys.exit(1)

# 2. 업비트 입금 주소 확인
print("업비트 ID 입금 주소 확인 중...", flush=True)
try:
    # fetch_deposit_address로 입금 주소 가져오기
    deposit_info = upbit.fetch_deposit_address('ID')
    address = deposit_info['address']
    tag = deposit_info.get('tag', None)

    print(f"  주소: {address}", flush=True)
    if tag:
        print(f"  태그/메모: {tag}", flush=True)
    print()

except Exception as e:
    print(f"❌ 입금 주소 조회 실패: {e}", flush=True)
    print("수동으로 업비트에서 ID 입금 주소를 확인하세요.", flush=True)
    sys.exit(1)

# 3. OKX 출금 수수료 및 최소 출금량 확인
print("OKX 출금 정보 확인 중...", flush=True)
try:
    currencies = okx.fetch_currencies()
    id_info = currencies.get('ID', {})

    withdraw_fee = id_info.get('fee', 'unknown')
    withdraw_min = id_info.get('limits', {}).get('withdraw', {}).get('min', 'unknown')

    print(f"  출금 수수료: {withdraw_fee}", flush=True)
    print(f"  최소 출금량: {withdraw_min}\n", flush=True)

except Exception as e:
    print(f"  정보 확인 실패: {e}", flush=True)
    print("  계속 진행...\n", flush=True)

# 4. 출금 실행
transfer_amount = okx_id * 0.99  # 99% 전송 (수수료 여유)

print(f"{transfer_amount:.2f}개 전송 시작...", flush=True)
confirm = input("계속하시겠습니까? (yes/no): ")

if confirm.lower() != 'yes':
    print("취소됨", flush=True)
    sys.exit(0)

try:
    # OKX에서 출금
    params = {}
    if tag:
        params['tag'] = tag

    result = okx.withdraw('ID', transfer_amount, address, params=params)

    print(f"✅ 출금 요청 완료", flush=True)
    print(f"  TX ID: {result.get('id', 'N/A')}", flush=True)
    print(f"  상태: {result.get('status', 'N/A')}", flush=True)
    print(f"\n⏱️  블록체인 전송 중... (약 30분 소요)", flush=True)
    print(f"  업비트에서 입금 확인: https://upbit.com/mypage/wallet/deposit/ID", flush=True)

except Exception as e:
    print(f"❌ 출금 실패: {e}", flush=True)
    print(f"오류 타입: {type(e).__name__}", flush=True)
