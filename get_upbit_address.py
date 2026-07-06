#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
업비트 입금 주소 조회 (직접 API)
"""
import os
import requests
from dotenv import load_dotenv
from upbit_auth import generate_upbit_token

load_dotenv()

access_key = os.getenv('UPBIT_ACCESS_KEY')
secret_key = os.getenv('UPBIT_SECRET_KEY')
api_url = 'https://api.upbit.com'

def get_deposit_address(currency):
    """입금 주소 조회"""
    query_params = {'currency': currency}
    token = generate_upbit_token(access_key, secret_key, query_params)
    headers = {'Authorization': f'Bearer {token}'}

    from urllib.parse import urlencode
    query_string = urlencode(query_params)

    response = requests.get(
        api_url + f'/v1/deposits/coin_addresses?{query_string}',
        headers=headers
    )

    if response.status_code == 200:
        data_list = response.json()
        if data_list and len(data_list) > 0:
            data = data_list[0]  # 첫 번째 주소 사용
            return {
                'address': data.get('deposit_address'),
                'tag': data.get('secondary_address')
            }
        else:
            raise Exception(f"입금 주소가 없습니다")
    else:
        raise Exception(f"주소 조회 실패: {response.json()}")

# 테스트
print("=== 업비트 입금 주소 조회 ===\n")

for coin in ['BAT', 'ID']:
    try:
        info = get_deposit_address(coin)
        print(f"{coin}:")
        print(f"  주소: {info['address']}")
        if info['tag']:
            print(f"  태그: {info['tag']}")
        print()
    except Exception as e:
        print(f"{coin}: {e}\n")
