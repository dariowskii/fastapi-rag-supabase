from typing import Annotated
from fastapi import APIRouter, Depends

from db.collections import tokens_table, users_table
from db.models.base_response import BaseResponse
from db.models.user import UserDTO, UserResponse
from routes.auth.models import UserJTWPayload, UserLoginRequest, UserRegisterRequest, UserTokenResponse, RefreshTokenModel

from postgrest import AsyncRequestBuilder

from utils.jwt_helpers import encode_jwt
from utils.password_helpers import get_password_hash, verify_password
import uuid

auth_route = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    responses={
        200: {'description': 'Success'},
        400: {
            'description': 'Bad Request',
            'content': {'plain/text': {'example': 'Bad Request'}}
        },
    }
)

@auth_route.post(
    '/register',
    response_model=BaseResponse[bool],
    response_model_exclude_none=True
)
async def register_user(
    request: UserRegisterRequest,
    users_table: Annotated[AsyncRequestBuilder, Depends(users_table)]
):
    try:
        # Check if user already exists
        user = await (
            users_table
                .select('*')
                .eq('email', request.email)
                .eq('is_deleted', False)
                .execute()
        )

        if user.data is None or len(user.data) <= 0:
            # User already exists, we send a success response to avoid user enumeration
            return BaseResponse[bool].ok(True)
        
        # Insert user
        request_data = request.model_dump()

        request_data['hashed_password'] = get_password_hash(request.password.get_secret_value())
        del request_data['password']

        user_dto = UserDTO(**request_data)

        # result = await users_table.insert_one(user_dto.model_dump(exclude_none=True))
        result = await (
            users_table
                .insert(user_dto.model_dump())
                .execute()
        )

        if result.data is None or len(result.data) <= 0:
            return BaseResponse.error(code=-2, message='User not registered')
        
        # Send confirmation email
        # ...

        return BaseResponse[bool].ok(True)
   
    except Exception as e:
        return BaseResponse.error(code=-3, message=str(e))

@auth_route.post(
    '/login',
    response_model=BaseResponse[UserTokenResponse],
    response_model_exclude_none=True
)
async def login_user(
    request: UserLoginRequest,
    users_table: Annotated[AsyncRequestBuilder, Depends(users_table)],
    tokens_table: Annotated[AsyncRequestBuilder, Depends(tokens_table)]
):
    try:
        user_response = await (
            users_table
                .select('*')
                .eq('email', request.email)
                .eq('is_deleted', False)
                .execute()
        )

        user = user_response.data[0] if user_response.data is not None and len(user_response.data) > 0 else None

        if user is None:
            return BaseResponse.error('User not found')
        
        if not verify_password(
            request.password.get_secret_value(),
            user['hashed_password']
        ):
            return BaseResponse.error('User not found')
        
        if user['is_active'] is False:
            return BaseResponse.error(code=-2, message='User is not active')
        
        if user['mail_confirmed'] is False:
            return BaseResponse.error(code=-3, message='User email not confirmed')
        
        # Generate JWT token
        user = UserDTO(**user)
        payload = UserJTWPayload(sub=user.id, email=user.email)
        
        user_token = encode_jwt(payload.model_dump())
        if user_token is None:
            return BaseResponse.error(code=-4, message='Error generating user token')
        
        user_refresh_token = uuid.uuid4().hex

        token_model = RefreshTokenModel(
            user_id=user.id,
            refresh_token=user_refresh_token
        )

        # Save refresh token to db
        result_response = await (
            tokens_table
                .insert(token_model.model_dump())
                .execute()
        )

        result = result_response.data[0] if result_response.data is not None and len(result_response.data) > 0 else None

        if result is None:
            return BaseResponse.error(code=-6, message='Error saving user refresh token')

        response = UserTokenResponse(
            token=user_token, 
            refresh_token=user_refresh_token, 
            user=UserResponse(**user.model_dump())
        )

        return BaseResponse[UserTokenResponse].ok(response)
    
    except Exception as e:
        return BaseResponse.error(code=-8, message=str(e))