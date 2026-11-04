import uuid
from datetime import datetime
from sqlalchemy import String,Integer, DateTime, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class ToolCall(Base):
    __tablename__ = 'tool_calls'

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key= True, default =uuid.uuid4)

    session_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True),ForeignKey('sessions.id', ondelete='CASCADE'))

    tool_name : Mapped[str] =mapped_column(String(50), nullable=False)

    args : Mapped[dict] = mapped_column(JSONB, nullable=False)

    result : Mapped[dict] = mapped_column(JSONB, nullable= False)

    latency_ms : Mapped[int] = mapped_column(Integer, nullable=False)

    success : Mapped[bool] = mapped_column(Boolean, default =True)

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone =True),server_default=func.now())