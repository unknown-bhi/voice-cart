from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.db import get_db
from app.modules.tools.schemas import ToolCallCreate
from app.modules.tools.service import save_tool_log

router = APIRouter(prefix="/session", tags=["Tools"])

@router.post("/{session_id}/tool-log", status_code=201)
async def api_save_tool_log(session_id: UUID, payload: ToolCallCreate, db: AsyncSession = Depends(get_db)):
    await save_tool_log(db, session_id, payload)
    return {"ok": True}