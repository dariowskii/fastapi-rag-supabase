from pydantic import BaseModel


class RagResponse(BaseModel):
    list: list[str]