from fastapi import status
from fastapi.routing import APIRouter
import httpx

from ...utils import (
    create_access_token,
    create_refresh_token
)
from ...core.config import ACCOUNT_ENDPOINT
from ...schema.schemas import UserRequest, TokenResponse


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
