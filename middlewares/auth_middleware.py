from typing import Annotated
from db.collections import users_table
from db.models.user import UserDTO
from fastapi import Depends, Header, HTTPException
from utils.jwt_helpers import decode_jwt
from postgrest import AsyncRequestBuilder

async def auth_user_middleware(
    users_table: Annotated[AsyncRequestBuilder, Depends(users_table)],
    authorization: Annotated[str, Header()]
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.split(" ")[1]
    user_dict = decode_jwt(token)

    if not user_dict:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_id = user_dict['sub']
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        user = await (
            users_table
                .select('*')
                .eq('id', user_id)
                .eq('is_deleted', False)
                .execute()
        )
        if user is None:
            return None
        
        return UserDTO(**user)
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")