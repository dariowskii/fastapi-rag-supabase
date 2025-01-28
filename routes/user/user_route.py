from fastapi import APIRouter, Depends
from typing import List, Annotated

from db.models.user import UserResponse, UserPatchRequest
from db.models.base_response import BaseResponse
from db.collections import users_table

from postgrest import AsyncRequestBuilder

user_route = APIRouter(
    prefix='/user', 
    tags=['User'],
    responses={
        200: {'description': 'Success'},
        400: {
            'description': 'Bad Request',
            'content': {'plain/text': {'example': 'Bad Request'}}
        },
    }
)

@user_route.get(
    '/{user_id}',
    response_model=BaseResponse[UserResponse],
    response_model_exclude_none=True
)
async def get_user(
    user_id: int, 
    users_table: Annotated[AsyncRequestBuilder, Depends(users_table)]
):
    try:
        user = await (
            users_table
                .select('*')
                .eq('id', user_id)
                .eq('is_deleted', False)
                .execute()
        )

        user = user.data[0] if user.data is not None and len(user.data) > 0 else None

        if user is None:
            return BaseResponse[UserResponse].error('User not found')
        
        return BaseResponse[UserResponse].ok(user)
    except:
        return BaseResponse[UserResponse].error('User not found')

@user_route.patch(
    '/{user_id}',
    response_model=BaseResponse[UserResponse],
    response_model_exclude_none=True
)
async def patch_user(
    user_id: int,
    user_data: UserPatchRequest,
    users_table: Annotated[AsyncRequestBuilder, Depends(users_table)]
):
    try:
        user = await (
            users_table
                .update(user_data.model_dump(exclude_unset=True))
                .eq('id', user_id)
                .eq('is_deleted', False)
                .execute()
        )

        user = user.data[0] if user.data is not None and len(user.data) > 0 else None

        if user is None:
            return BaseResponse[UserResponse].error('User not patched')
        
        return BaseResponse[UserResponse].ok(user)
    except:
        return BaseResponse[UserResponse].error('User not patched')

@user_route.delete(
    '/{user_id}',
    response_model=BaseResponse[bool],
    response_model_exclude_none=True
)
async def delete_user(
    user_id: int, 
    users_table: Annotated[AsyncRequestBuilder, Depends(users_table)]
):
    try:
        result = await (
            users_table
                .update({'is_deleted': True})
                .eq('id', user_id)
                .eq('is_deleted', False)
                .execute()
        )

        if not result:
            return BaseResponse.error('User not deleted')
        
        return BaseResponse.ok(True)
    except:
        return BaseResponse.error('User not deleted')