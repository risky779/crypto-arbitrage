#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
빗썸 API 간단 테스트
"""
import os
import requests
from dotenv import load_dotenv
from auth import generate_token

load_dotenv()

access_key = os.getenv('BITHUMB_API_KEY')
secret_key = os.getenv('BITHUMB_SECRET_KEY')

print(f"API Key: {access_key}")
print(f"Secret Key: {secret_key[:20]}...")

# 토큰 생성
token = generate_token(access_key, secret_key, '')

print(f"\nToken (앞 50자): {token[:50]}...")

# 잔고 조회 시도
headers = {'Authorization': f'Bearer {token}'}

print("\n엔드포인트 1: /v1/accounts")
response1 = requests.get('https://api.bithumb.com/v1/accounts', headers=headers)
print(f"Status: {response1.status_code}")
print(f"Response: {response1.text[:200]}")

print("\n엔드포인트 2: /info/balance")
response2 = requests.post('https://api.bithumb.com/info/balance', headers=headers)
print(f"Status: {response2.status_code}")
print(f"Response: {response2.text[:200]}")

print("\n엔드포인트 3: /info/account")
response3 = requests.post('https://api.bithumb.com/info/account', headers=headers)
print(f"Status: {response3.status_code}")
print(f"Response: {response3.text[:200]}")
