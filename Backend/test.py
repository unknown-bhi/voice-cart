from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.modules.connectors.service import create_connector,delete_connector
from app.modules.connectors.schemas import ConnectorCreateRequest,ConnectorResponse

router = APIRouter(prefix ='/connectors', tags = ['Connectors'])

@router.post('', response_model =ConnectorResponse,status_code=status.HTTP_201_CREATED )
async def api_create_connector(
    payload: ConnectorCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    return await create_connector(db, payload)

@router.delete('/{connector_id}' , status_code =status.HTTP_200_OK)
async def api_delete_connector(
    connector_id :UUID,
    db: AsyncSession =Depends(get_db)
):
    success = await delete_connector(db, connector_id)
    if not success:
        raise HTTPException(status_code= 404, detail = 'Connector not found')

    return {'status' : 'deleted'}