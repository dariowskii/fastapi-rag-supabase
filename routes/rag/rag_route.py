from fastapi import APIRouter, Depends, UploadFile
from typing import List, Annotated

from supabase import AsyncClient

from db.config import db_connection
from db.models.user import UserResponse, UserPatchRequest
from db.models.base_response import BaseResponse
from db.collections import users_table
from middlewares.auth_middleware import auth_user_middleware
from routes.rag.models import RagResponse

from postgrest import AsyncRequestBuilder

rag_route = APIRouter(
    prefix='/rag', 
    tags=['Rag'],
    responses={
        200: {'description': 'Success'},
        400: {
            'description': 'Bad Request',
            'content': {'plain/text': {'example': 'Bad Request'}}
        },
    }
)

@rag_route.post(
    '/upload-document',
    response_model=BaseResponse[bool],
    response_model_exclude_none=True,
)
async def upload_document(
    file: UploadFile
):
    pass

@rag_route.post(
    '/search',
    response_model=BaseResponse[RagResponse],
    response_model_exclude_none=True,
)
async def search(
    query: str,
    supabase: Annotated[AsyncClient, Depends(db_connection)]
):
    query_embedding = []
    
    rag_results = await (
        supabase.functions.invoke(
            'match_filtered_document_sections',
            {
                'body': {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.5,
                    'match_count': 5,
                    'owner_id': 3
                }
            }
        )
    )

    print(rag_results)

    if not rag_results:
        return BaseResponse[RagResponse].error('No results found')
    
    return BaseResponse[RagResponse].ok(RagResponse(list=[]))