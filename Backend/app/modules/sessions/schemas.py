from pydantic import BaseModel, Field
from uuid import UUID

class SessionCreateRequest(BaseModel):

    user_id : str =Field(..., min_length=1, max_length=100,examples =['user_1234']),

class SessionCreateResponse(BaseModel):

    session_id : UUID =Field(...,)
    token : str =Field(...,)
    room_name : str =Field(...,)
    ws_url : str  =Field(...,)

class SessionEndResponse(BaseModel):

    status : str =Field(..., examples =['ended'])


class InterruptionUpdateRequest(BaseModel):

    room_name : str 

