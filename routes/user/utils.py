from postgrest import AsyncRequestBuilder
from pydantic import EmailStr

from db.models.user import UserDTO

async def get_user_by_email(user_email: EmailStr, users_table: AsyncRequestBuilder) -> UserDTO | None:
    try:
        user = await (
            users_table
                .select('*')
                .eq('email', user_email)
                .eq('is_deleted', False)
                .execute()
        )
        if user is None:
            return None
        
        return UserDTO(**user)
    except:
        return None