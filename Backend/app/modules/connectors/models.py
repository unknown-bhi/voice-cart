import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class Connector(Base):
    __tablename__ = 'connectors'

    id :Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    user_id : Mapped[str] = mapped_column(String(100), nullable =False)

    platform : Mapped[str] = mapped_column(String(20), nullable =False)

    display_name : Mapped[str] = mapped_column(String(100), nullable =False)

    credentials_encrypted: Mapped[bytes] = mapped_column(BYTEA, nullable =True)

    mcp_server_url : Mapped[str] =mapped_column(String(255), nullable=True)

    status : Mapped[str] = mapped_column(String(20), default ='pending')

    last_sync_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at : Mapped[datetime] =mapped_column(DateTime(timezone=True), server_default=func.now())


    def __repr__(self):
        return f"<Connector platform={self.platform} status={self.status}>"