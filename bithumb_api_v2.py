#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
빗썸 API 2.0 거래 모듈
"""
import os
import requests
import json
from dotenv import load_dotenv
from auth import generate_token

load_dotenv()


class BithumbAPIv2:
    def __init__(self):
        self.api_key = os.getenv('BITHUMB_API_KEY')
        self.secret_key = os.getenv('BITHUMB_SECRET_KEY')
        self.api_url = 'https://api.bithumb.com'

    def get_balance(self):
        """잔고 조회"""
        query = ''
        token = generate_token(self.api_key, self.secret_key, query)
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.get(self.api_url + '/v1/accounts', headers=headers)

        if response.status_code == 200:
            accounts = response.json()
            balance = {}
            for acc in accounts:
                balance[acc['currency']] = {
                    'free': float(acc['balance']),
                    'locked': float(acc['locked'])
                }
            return balance
        else:
            raise Exception(f"잔고 조회 실패: {response.json()}")

    def market_buy(self, market, amount_krw):
        """
        시장가 매수

        Args:
            market: 거래 페어 (예: 'KRW-BTC')
            amount_krw: 매수 금액 (KRW)

        Returns:
            주문 결과
        """
        request_body = {
            'market': market,
            'side': 'bid',
            'order_type': 'price',  # 시장가 매수 (금액 지정)
            'price': str(int(amount_krw)),
        }

        # body 파라미터를 쿼리 문자열로 변환하여 해싱
        query = '&'.join([f'{k}={v}' for k, v in request_body.items()])
        token = generate_token(self.api_key, self.secret_key, query)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

        response = requests.post(
            self.api_url + '/v2/orders',
            data=json.dumps(request_body),
            headers=headers,
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"매수 실패: {response.json()}")

    def market_sell(self, market, volume):
        """
        시장가 매도

        Args:
            market: 거래 페어 (예: 'KRW-BTC')
            volume: 매도 수량

        Returns:
            주문 결과
        """
        request_body = {
            'market': market,
            'side': 'ask',
            'order_type': 'market',  # 시장가 매도
            'volume': str(volume),
        }

        query = '&'.join([f'{k}={v}' for k, v in request_body.items()])
        token = generate_token(self.api_key, self.secret_key, query)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

        response = requests.post(
            self.api_url + '/v2/orders',
            data=json.dumps(request_body),
            headers=headers,
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"매도 실패: {response.json()}")

    def get_order(self, order_id):
        """주문 조회"""
        query = f'order_id={order_id}'
        token = generate_token(self.api_key, self.secret_key, query)
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.get(
            self.api_url + f'/v2/order?{query}',
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"주문 조회 실패: {response.json()}")

    def withdraw(self, currency, amount, address, net_type, secondary_address=None, exchange_name=None, receiver_type=None, receiver_ko_name=None, receiver_en_name=None):
        """
        출금 (코인 전송)

        Args:
            currency: 코인 심볼 (예: 'BTC')
            amount: 출금 수량
            address: 입금 주소
            net_type: 출금 네트워크 (예: 'SUI', 'ETH', 'BSC' 등)
            secondary_address: 2차 주소 (XRP 태그 등, 선택)
            exchange_name: 수신 거래소 영문명 (선택)
            receiver_type: 수신인 타입: 'personal' 또는 'corporation' (선택)
            receiver_ko_name: 수신인 한글 이름 (선택)
            receiver_en_name: 수신인 영문 이름 (선택)

        Returns:
            출금 결과
        """
        request_body = {
            'currency': currency,
            'amount': str(amount),
            'address': address,
            'net_type': net_type,
        }

        if secondary_address:
            request_body['secondary_address'] = secondary_address
        if exchange_name:
            request_body['exchange_name'] = exchange_name
        if receiver_type:
            request_body['receiver_type'] = receiver_type
        if receiver_ko_name:
            request_body['receiver_ko_name'] = receiver_ko_name
        if receiver_en_name:
            request_body['receiver_en_name'] = receiver_en_name

        query = '&'.join([f'{k}={v}' for k, v in request_body.items()])
        token = generate_token(self.api_key, self.secret_key, query)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

        response = requests.post(
            self.api_url + '/v1/withdraws/coin',
            data=json.dumps(request_body),
            headers=headers,
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"출금 실패: {response.json()}")


if __name__ == '__main__':
    # 테스트
    api = BithumbAPIv2()

    print("=== 빗썸 API 2.0 테스트 ===\n")

    # 잔고 조회
    balance = api.get_balance()
    krw = balance.get('KRW', {}).get('free', 0)
    print(f"KRW 잔고: {krw:,.2f}원")
    print("\n✅ 빗썸 API 2.0 연동 완료!")
