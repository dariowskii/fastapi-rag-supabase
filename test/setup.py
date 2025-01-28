from fastapi.testclient import TestClient
# from mongomock_motor import AsyncMongoMockClient
# from db.config import DBConnectionError, db_connection
from main import app

client = TestClient(app)
# fake_db = AsyncMongoMockClient()['test_db']

# def override_db_connection():
#     try:
#         yield fake_db
#     except Exception as e:
#         raise DBConnectionError(f"DB connection error: {e}")
    
# app.dependency_overrides[db_connection] = override_db_connection
