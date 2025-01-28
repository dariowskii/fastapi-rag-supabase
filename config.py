from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings
from pydantic import Secret
import os

load_dotenv()

# -------
# CONFIG
# -------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

JWT_SECRET = Secret(os.getenv("JWT_SECRET", default="secret"))
JWT_REFRESH_SECRET = Secret(os.getenv("JWT_REFRESH_SECRET", default="refresh_secret"))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", default="HS256")
JWT_EXPIRATION_SECONDS = int(os.getenv("JWT_EXPIRATION_SECONDS", default=60))

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", "*"))

PASSWORD_SALT = os.getenv("PASSWORD_SALT", default="salt")

# ------------
# TABLES
# ------------

USERS_TABLE = "users"
TOKENS_TABLE= "tokens"
