import uuid 
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class Utterance(Base):
    __tablename__ = 'utternaces'

    id: Mapped[int] =mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey('sessions.id', ondelete= 'CASCADE'))

    role: Mapped[str] = mapped_column(String(10), nullable =False)

    text : Mapped[str] =mapped_column(String, nullable =False)

    start_ms : Mapped[int] =mapped_column(Integer, nullable=True)

    end_ms : Mapped[int] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())

    def __reper__(self):
        return f'<Utterance role ={self.role} : text ={self.text[:20]}.....>'