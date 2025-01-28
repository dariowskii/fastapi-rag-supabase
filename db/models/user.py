import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from db.types import UTCDatetime

class UserDTO(BaseModel):
    id: int 
    name: str
    surname: str
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    updated_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    deleted_at: float | None = None
    is_active: bool = True
    is_deleted: bool = False
    mail_confirmed: bool = False

class UserPatchRequest(BaseModel):
    name: str | None = None
    surname: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'John',
                'surname': 'Doe'
            }
        }
    )

class UserRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    hashed_password: str

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'John',
                'surname': 'Doe'
            }
        }
    )

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    created_at: UTCDatetime
    updated_at: UTCDatetime
    is_active: bool
    mail_confirmed: bool

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'id': '60f1e1b7b6f1b1b3f3b3b3b3',
                'name': 'John',
                'surname': 'Doe',
                'email': 'mail@mail.com',
                'created_at': '2021-07-17T00:00:00Z',
                'updated_at': '2021-07-17T00:00:00Z',
                'is_active': True,
                'mail_confirmed': False
            }
        }
    )