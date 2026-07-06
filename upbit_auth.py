"""
업비트 API JWT 인증 토큰 생성
"""
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

def generate_upbit_token(access_key, secret_key, query_params=None):
    """
    업비트 JWT 인증 토큰을 생성합니다.

    Args:
        access_key: 발급받은 Access Key
        secret_key: 발급받은 Secret Key
        query_params: 쿼리 파라미터 딕셔너리

    Returns:
        JWT 토큰 문자열
    """
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    if query_params:
        query_string = urlencode(query_params).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload['query_hash'] = query_hash
        payload['query_hash_alg'] = 'SHA512'

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
