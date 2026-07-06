"""
빗썸 API JWT 인증 토큰 생성
"""
import jwt
import uuid
import hashlib
from datetime import datetime

def generate_token(access_key, secret_key, query=''):
    """
    JWT 인증 토큰을 생성합니다.

    Args:
        access_key: 발급받은 Access Key
        secret_key: 발급받은 Secret Key
        query: 쿼리 문자열 (파라미터가 없으면 빈 문자열)

    Returns:
        JWT 토큰 문자열
    """
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'timestamp': int(datetime.now().timestamp() * 1000),
    }

    if query:
        m = hashlib.sha512()
        m.update(query.encode('utf-8'))
        payload['query_hash'] = m.hexdigest()
        payload['query_hash_alg'] = 'SHA512'

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
