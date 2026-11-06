from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.modules.tools.models import ToolCall
from app.modules.tools.schemas import ToolCallCreate

async def save_tool_log(db: AsyncSession, session_id: UUID, payload: ToolCallCreate):
    log = ToolCall(
        session_id=session_id,
        tool_name=payload.tool_name,
        args=payload.args,
        result=payload.result,
        latency_ms=payload.latency_ms,
        success=payload.success
    )
    db.add(log)
    await db.commit()