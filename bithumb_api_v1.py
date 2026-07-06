#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
빗썸 API 1.0 (구버전) 인증 및 거래
"""
import os
import time
import hmac
import hashlib
import urllib.parse
import base64
import requests
from dotenv import load_dotenv

load_dotenv()


class BithumbAPIv1:
    def __init__(self):
        self.api_key = os.getenv('BITHUMB_API_KEY')
        # Secret Key는 Base64로 인코딩되어 있을 수 있음
        secret_key_str = os.getenv('BITHUMB_SECRET_KEY')
        try:
            self.secret_key = base64.b64decode(secret_key_str)
        except:
            self.secret_key = secret_key_str.encode('utf-8')
        self.api_url = 'https://api.bithumb.com'

    def _signature(self, endpoint, params):
        """HMAC-SHA512 서명 생성"""
        # nonce 생성 (microseconds)
        nonce = str(int(time.time() * 1000))

        # 파라미터를 쿼리 스트링으로 변환 (endpoint 제외)
        query_string = urllib.parse.urlencode(params)

        # 서명할 데이터: endpoint + chr(0) + query_string + chr(0) + nonce
        sign_data = endpoint + chr(0) + query_string + chr(0) + nonce

        # HMAC-SHA512 서명
        signature = hmac.new(
            self.secret_key if isinstance(self.secret_key, bytes) else self.secret_key.encode('utf-8'),
            sign_data.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()

        return signature, nonce

    def _request(self, endpoint, params=None):
        """Private API 요청"""
        if params is None:
            params = {}

        # 서명 생성
        signature, nonce = self._signature(endpoint, params)

        # 헤더 설정
        headers = {
            'Api-Key': self.api_key,
            'Api-Sign': signature,
            'Api-Nonce': nonce,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # POST 요청
        response = requests.post(
            self.api_url + endpoint,
            headers=headers,
            data=params
        )

        return response.json()

    def get_balance(self, currency='ALL'):
        """잔고 조회"""
        endpoint = '/info/balance'
        params = {'currency': currency}
        return self._request(endpoint, params)

    def get_account(self, order_currency='BTC', payment_currency='KRW'):
        """계좌 정보 조회"""
        endpoint = '/info/account'
        params = {
            'order_currency': order_currency,
            'payment_currency': payment_currency
        }
        return self._request(endpoint, params)

    def market_buy(self, order_currency, units=None, price=None):
        """
        시장가 매수

        Args:
            order_currency: 주문 통화 (예: 'BTC')
            units: 매수 수량 (선택)
            price: 매수 금액 (KRW, 선택)

        Note: units 또는 price 중 하나만 입력
        """
        endpoint = '/trade/market_buy'
        params = {
            'order_currency': order_currency,
            'payment_currency': 'KRW'
        }

        if units:
            params['units'] = str(units)
        if price:
            params['price'] = str(int(price))

        return self._request(endpoint, params)

    def market_sell(self, order_currency, units):
        """
        시장가 매도

        Args:
            order_currency: 주문 통화 (예: 'BTC')
            units: 매도 수량
        """
        endpoint = '/trade/market_sell'
        params = {
            'order_currency': order_currency,
            'payment_currency': 'KRW',
            'units': str(units)
        }

        return self._request(endpoint, params)


if __name__ == '__main__':
    # 테스트
    api = BithumbAPIv1()

    print("=== 빗썸 API 1.0 테스트 ===")

    # 잔고 조회
    print("\n1. 잔고 조회:")
    balance = api.get_balance()
    print(f"Status: {balance.get('status')}")

    if balance.get('status') == '0000':
        print("✅ API 연결 성공!")
        data = balance.get('data', {})
        krw = data.get('total_krw', 0)
        print(f"총 자산(KRW): {krw}원")

        # 개별 코인 잔고
        available_krw = data.get('available_krw', 0)
        print(f"사용 가능 KRW: {available_krw}원")
    else:
        print(f"❌ 오류: {balance.get('message')}")
