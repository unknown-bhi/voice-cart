import uuid
from datetime import datetime
from sqlalchemy import String,Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import Mapped,mapped_column

from app.core.db import Base

class Session(Base):
    __tablename__ ='sessions'

    id :Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)

    user_id :Mapped[str] = mapped_column(String(100), nullable =False)

    room_name:Mapped[str] = mapped_column(String(100),unique=True, nullable=False)

    status :Mapped[str] =mapped_column(String(20),default='active',nullable =False)

    started_at :Mapped[datetime] =mapped_column(DateTime(timezone=True),server_default=func.now())

    ended_at :Mapped[datetime | None] = mapped_column(DateTime(timezone=True,),nullable=True) 

    avg_latency_ms: Mapped[int | None] =mapped_column(Integer, nullable =True)

    interruption_count :Mapped[int] =mapped_column(Integer, nullable=False , default=0)


    def __repr__(self):
        return f"Session id = {self.id}  user_id = {self.id}  status = {self.status} :" 
    