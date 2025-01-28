from typing import Annotated
from config import TOKENS_TABLE, USERS_TABLE
from db.config import db_connection
from fastapi import Depends

from supabase import AsyncClient
from postgrest import AsyncRequestBuilder

def users_table(db: Annotated[AsyncClient, Depends(db_connection)]) -> AsyncRequestBuilder:
    return db.table(USERS_TABLE)

def tokens_table(db: Annotated[AsyncClient, Depends(db_connection)]) -> AsyncRequestBuilder:
    return db.table(TOKENS_TABLE)