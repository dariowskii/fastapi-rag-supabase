
from routes.user.user_route import get_user
from routes.user.utils import get_user_by_email
from utils.password_helpers import verify_password
from postgrest import AsyncRequestBuilder

async def authenticate_user(user_collection: AsyncRequestBuilder, username: str, password: str):
    user = await get_user_by_email(username, user_collection)
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user