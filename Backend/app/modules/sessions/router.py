from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


from app.core.db import get_db
from app.modules.sessions.schemas import(
    SessionCreateRequest,SessionEndResponse,SessionCreateResponse,
    InterruptionUpdateRequest
)

from app.modules.sessions.service import (
    create_session,
    end_session,
    MaxSessionReachedError,
    SessionNotFoundError,
    record_interruption
)
from sqlalchemy import select
from app.modules.sessions.models import Session

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


@router.post('/interruption',status_code=status.HTTP_200_OK, include_in_schema=False)
async def api_record_interruption(
    payload: InterruptionUpdateRequest, db: AsyncSession =Depends(get_db)
):
    
    await record_interruption(db, payload.room_name)
    return {'ok' : True} 


@router.get('/by-room/{room_name}', include_in_schema=False)
async def get_session_by_room(room_name: str, db : AsyncSession = Depends(get_db)):

    stmt = select(Session).where(Session.room_name == room_name)
    result = await db.execute(stmt)

    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail = 'Session not found')
    return {'session_id' : str(session.id)}
