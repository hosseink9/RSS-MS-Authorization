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


