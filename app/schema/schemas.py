from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str
    firstname: str | None=None
    lastname: str | None=None


class UserResponse(BaseModel):
    id: str
    username: str
    firstname: str | None=None
    lastname: str | None=None



class UserUpdate(BaseModel):
    username: str | None=None
    firstname: str | None=None
    lastname: str | None=None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str