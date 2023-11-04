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
from ...core.config import ACCOUNT_ENDPOINT, CREATE_OTP_ENDPOINT, VERIFY_OTP_ENDPOINT
from ...schema.schemas import Otp, UserRequest, TokenResponse
from ...db.db import RedisDB

router = APIRouter(tags=["authorization"])


@router.post("/send_otp", status_code=status.HTTP_200_OK)
async def send_otp(user: UserRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{ACCOUNT_ENDPOINT}/login', json=user.dict())
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

    async with httpx.AsyncClient() as client:
        result = await client.post(CREATE_OTP_ENDPOINT, json=response.json())

    return result.json()


@router.post("/verify_otp", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def verify_otp(otp: Otp):
    async with httpx.AsyncClient() as client:
        response = await client.post(VERIFY_OTP_ENDPOINT, json=otp.dict())
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                'Invalid otp !!')

    access_token = create_access_token(response.json())
    refresh_token = create_refresh_token(response.json())
    await refresh_token_store(refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/signup", status_code=status.HTTP_200_OK)
async def signup(user: UserRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{ACCOUNT_ENDPOINT}/signup', json=user.dict())
    return response.json()


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request):
    bearer = request.headers.get("Authorization")
    token = bearer.split(' ')[1]
    await delete_refresh_token(token)
    return {"detail": "logout"}
