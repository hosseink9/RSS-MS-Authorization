from datetime import datetime, timedelta
import os
from typing import Union, Any
from jose import jwt
from uuid import uuid4

from ..core import config
from ..db.db import RedisDB


def generate_jti():
    return str(uuid4().hex)


jti = generate_jti()


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    iat = datetime.utcnow()
    payload = {
        'user_id': subject,
        'exp': expires_delta,
        'iat': iat,
        'jti': jti
    }
    encode_jwt = jwt.encode(payload,
                            config.JWT_SECRET_KEY, config.ALGORITHM)
    return encode_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES)

    iat = datetime.utcnow()
    payload = {
        'user_id': subject,
        'exp': expires_delta,
        'iat': iat,
        'jti': jti
    }
    encoded_jwt = jwt.encode(
        payload, config.JWT_SECRET_KEY, config.ALGORITHM)
    return encoded_jwt


async def refresh_token_store(refresh_token):
    payload = jwt.decode(
        refresh_token, config.JWT_SECRET_KEY, algorithms=['HS256'])
    user_id = payload.get("user_id")
    jti = payload.get("jti")
    exp_date = payload.get('exp')
    iat = payload.get('iat')
    timeout = exp_date - iat
    redis = RedisDB()
    result = await redis.set_data(
        key=f"user_{user_id} | {jti}", value=exp_date, timeout=timeout)
    return result


async def delete_refresh_token(token):
    payload = jwt.decode(token, config.JWT_SECRET_KEY,
                         algorithms=[config.ALGORITHM])
    user_id = payload['user_id']

    jti = payload['jti']
    redis = RedisDB()
    await redis.delete_data(key=f"user_{user_id} | {jti}")
