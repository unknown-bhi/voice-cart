from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.modules.sessions.schemas import(
    SessionCreateRequest,SessionEndResponse,SessionCreateResponse
)

from app.modules.sessions.service import (
    create_session,
    end_session,
    MaxSessionReachedError,
    SessionNotFoundError
)

router =APIRouter(prefix='/session', tags=['Sessions'])

@router.post('/',response_model=SessionCreateResponse,status_code=status.HTTP_201_CREATED,)
async def api_create_session(payload: SessionCreateRequest, db:AsyncSession= Depends(get_db)):
    try:
        return await create_session(db=db,user_id =payload.user_id)
    except MaxSessionReachedError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )

@router.delete('/{session_id}',response_model=SessionEndResponse)
async def api_end_session(session_id:UUID,db: AsyncSession =Depends(get_db)):
    try:
        result_status = await end_session(db=db, session_id=session_id)
        return SessionEndResponse(status=result_status)

    except SessionNotFoundError as e:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail=str(e))

    