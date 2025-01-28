from pydantic import BaseModel, Secret, EmailStr
from db.models.user import UserResponse
import datetime

class UserRegisterRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: Secret[str]

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: Secret[str]

class UserJTWPayload(BaseModel):
    sub: str
    email: EmailStr

class UserTokenResponse(BaseModel):
    token: str
    refresh_token: str
    user: UserResponse

class RefreshTokenModel(BaseModel):
    user_id: int
    refresh_token: str
    expires_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)