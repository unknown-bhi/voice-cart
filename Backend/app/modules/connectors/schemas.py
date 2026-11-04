from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, Dict, Any
from datetime import datetime


class ConnectorCreateRequest(BaseModel):

    user_id : str =Field(...,)

    platform : str = Field(...,pattern= "^(shopify|daraz|generic)$")

    display_name : str= Field(..., )

    credentials : Dict[str , Any] = Field(..., )

    mcp_server_url : Optional[str] = Field(None, )

class ConnectorResponse(BaseModel):

    id : UUID
    user_id : str
    platform : str
    display_name : str
    mcp_server_url : Optional[str]
    status : str
    created_at :datetime

    class Config:
        from_attributes = True

        
