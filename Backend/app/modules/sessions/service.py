import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import check_and_register_session,remove_session
from app.core.livekit import generate_livekit_token
from app.core.config import settings
from app.modules.sessions.models import Session
from app.modules.sessions.schemas import SessionCreateResponse

class MaxSessionReachedError(Exception):
    'custom exceptio raised when user exceeds max concurrent sessions'
    pass

class SessionNotFoundError(Exception):
    'custom exception raised when a session ID doesnot exits'
    pass

async def create_session(db: AsyncSession, user_id: str):
    "create a new session, checks redis limits, generates token , and saves to DB"

    is_allowed =await check_and_register_session(user_id)

    if not is_allowed:
        raise MaxSessionReachedError('Maximum concurrent sessions (2) reached.')

    room_name = f'room-{uuid.uuid4().hex[:12]}'

    token = generate_livekit_token(user_id = user_id, room_name= room_name)

    new_session =Session(
        user_id=user_id,
        room_name=room_name,
        status='active'
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    return SessionCreateResponse(
        session_id= new_session.id,
        token=token,
        room_name=room_name,
        ws_url=settings.LIVEKIT_URL
    )

async def end_session(db: AsyncSession, session_id: uuid.UUID):

    session= await db.get(Session, session_id)
    if not session:
        raise SessionNotFoundError('Session not Found')

    if session.status == 'ended':
        return 'ended'

    session.status = 'ended'
    session.ended_at =datetime.now(timezone.utc)
    await db.commit()

    await remove_session(session.user_id)

    return 'ended'


    
