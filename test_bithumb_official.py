from dotenv import load_dotenv
import os
import requests
import json
from auth import generate_token

load_dotenv()

access_key = os.environ['BITHUMB_API_KEY']
secret_key = os.environ['BITHUMB_SECRET_KEY']
api_url = 'https://api.bithumb.com'

# 먼저 계좌 조회 시도
print("=== 계좌 조회 테스트 ===")
query = ''
token = generate_token(access_key, secret_key, query)
headers = {'Authorization': f'Bearer {token}'}

response = requests.get(api_url + '/v1/accounts', headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    accounts = response.json()
    for acc in accounts:
        if acc['currency'] == 'KRW':
            print(f"\nKRW 잔고: {acc['balance']}원")
