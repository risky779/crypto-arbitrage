#!/usr/bin/env python3
import ccxt, os, sys, io
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY')})

print("=== ID 코인 네트워크 정보 ===\n", flush=True)

try:
    # 업비트에서 ID 통화 정보 확인
    currencies = upbit.fetch_currencies()

    if 'ID' in currencies:
        id_info = currencies['ID']
        print(f"ID 정보:", flush=True)
        print(f"  이름: {id_info.get('name', 'N/A')}", flush=True)
        print(f"  네트워크: {id_info.get('networks', 'N/A')}", flush=True)
        print(f"  입출금 가능: {id_info.get('active', 'N/A')}", flush=True)
        print(f"  정보: {id_info}\n", flush=True)
    else:
        print("❌ ID 정보를 찾을 수 없음\n", flush=True)

    # OKX에서도 확인
    okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})

    okx_currencies = okx.fetch_currencies()
    if 'ID' in okx_currencies:
        okx_id_info = okx_currencies['ID']
        print(f"OKX ID 정보:", flush=True)
        print(f"  네트워크: {okx_id_info.get('networks', 'N/A')}", flush=True)
        print(f"  출금 수수료: {okx_id_info.get('fee', 'N/A')}", flush=True)
        print(f"  정보: {okx_id_info}", flush=True)

except Exception as e:
    print(f"❌ 오류: {e}", flush=True)
    import traceback
    traceback.print_exc()
