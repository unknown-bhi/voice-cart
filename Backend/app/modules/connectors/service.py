import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.connectors.models import Connector
from app.modules.connectors.schemas import ConnectorCreateRequest
from app.core.encryption import encrypt_data
from uuid import UUID

async def create_connector(db : AsyncSession, payload : ConnectorCreateRequest):

    creds_json = json.dumps(payload.credentials)
    encrypted_creds = encrypt_data(creds_json)

    new_connector =Connector(
        user_id=payload.user_id,
        platform=payload.platform,
        display_name=payload.display_name,
        credentials_encrypted=encrypted_creds,
        mcp_server_url = payload.mcp_server_url,
        status ='connected'
    )

    db.add(new_connector)
    await db.commit()
    await db.refresh(new_connector)

    return new_connector

async def delete_connector(db: AsyncSession, connector_id : UUID):

    connector = await db.get(Connector, connector_id)

    if not connector:
        return False

    await db.delete(connector)
    await db.commit()
    return True 
