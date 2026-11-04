from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.modules.transcripts.models import Utterance
from app.modules.transcripts.schemas import UtteranceCreate

async def save_utterance(db : AsyncSession, session_id : UUID, payload : UtteranceCreate):

    utterance = Utterance(
        session_id = session_id,
        role =payload.role,
        text = payload.text,
        start_ms=payload.start_ms,
        end_ms= payload.end_ms
        )

    db.add(utterance)
    await db.commit()
    