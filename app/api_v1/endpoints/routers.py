from fastapi import HTTPException, status, Request
from fastapi.routing import APIRouter
import httpx
from jose import jwt

from ...jwt.utils import (
    create_access_token,
    create_refresh_token,
    refresh_token_store,
    delete_refresh_token
)
from ...core.config import ACCOUNT_ENDPOINT
from ...schema.schemas import UserRequest, TokenResponse
from ...db.db import RedisDB

router = APIRouter(tags=["authorization"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(user: UserRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{ACCOUNT_ENDPOINT}/login', json=user.dict())
    return {
        "access_token": create_access_token(response.json()['id']),
        "refresh_token": create_refresh_token(response.json()['id'])
    }


@router.post("/signup", status_code=status.HTTP_200_OK)
async def signup(user: UserRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{ACCOUNT_ENDPOINT}/signup', json=user.dict())
    return response.json()
