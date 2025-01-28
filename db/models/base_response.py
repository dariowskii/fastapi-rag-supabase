from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str | None = None
    item: T | None = None

    @staticmethod
    def ok(item: T | None = None) -> dict:
        return BaseResponse(item=item).model_dump(exclude_none=True)
    
    @staticmethod
    def error(message: str, code: int = -1) -> dict:
        return BaseResponse(code=code, message=message).model_dump(exclude_none=True)