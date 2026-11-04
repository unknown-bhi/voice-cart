from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.db import get_db
from app.modules.transcripts.schemas import UtteranceCreate
from app.modules.transcripts.service import save_utterance
from sqlalchemy import select
from app.modules.transcripts.models import Utterance

router = APIRouter(prefix= '/session' ,tags= ['Transcripts'])

@router.post('/{session_id}/utterance', status_code=201)
async def api_save_utterance(session_id : UUID, payload : UtteranceCreate, db : AsyncSession =Depends(get_db)):

    await save_utterance(db, session_id , payload)
    return {'ok' : True}

@router.get('/{session_id}/transcript')
async def api_get_transcript(session_id : UUID, db : AsyncSession = Depends(get_db)):

    stmt = select(Utterance).where(Utterance.session_id == session_id).order_by(Utterance.created_at)
    result =await db.execute(stmt)
    messages = result.scalars().all()

    return {"session_id" : session_id, "messages" : [{"role" : m.role, "text" : m.text} for m in messages]}

