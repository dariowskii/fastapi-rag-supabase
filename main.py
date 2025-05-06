from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.user.user_route import user_route
from routes.auth.auth_route import auth_route
from routes.rag.rag_route import rag_route

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from config import ALLOWED_HOSTS
from pydantic import ConfigDict
import datetime
from utils.remove_422 import remove_422s

# -------------
# CONFIGURATION
# -------------

app = FastAPI(
    title='RAG test API',
    description='API for RAG test',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ConfigDict.json_encoders = {
    datetime.datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%SZ')
}

# -------------
#    ROUTES
# -------------

app.include_router(user_route)
app.include_router(auth_route)
app.include_router(rag_route)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = exc.errors()

    errors_plain = []
    for error in errors:
        errors_plain.append(error['ctx']['reason'])

    return PlainTextResponse(';'.join(errors_plain), status_code=400)

remove_422s(app)