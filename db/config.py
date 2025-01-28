from config import SUPABASE_KEY, SUPABASE_URL
from supabase import AsyncClient, create_async_client

class DBConnectionError(Exception):
    pass

async def db_connection():
    """DB connection context manager

    Raises:
        DBConnectionError: The DB connection error

    Yields:
        AsyncClient: The Supabase client
    """

    supabaseConnection: AsyncClient = await create_async_client(SUPABASE_URL, SUPABASE_KEY)

    try:
        yield supabaseConnection
    except Exception as e:
        raise DBConnectionError(f"DB connection error: {e}")