from supabase import create_async_client
from config import SUPABASE_KEY, SUPABASE_URL

supabaseConnection = create_async_client(SUPABASE_URL, SUPABASE_KEY)

class DBConnectionError(Exception):
    pass

async def db_connection():
    """DB connection context manager

    Raises:
        DBConnectionError: The DB connection error

    Yields:
        AsyncClient: The Supabase client
    """

    try:
        yield await supabaseConnection
    except Exception as e:
        raise DBConnectionError(f"DB connection error: {e}")