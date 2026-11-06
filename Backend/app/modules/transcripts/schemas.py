from pydantic import BaseModel

class UtteranceCreate(BaseModel):

    role : str
    text : str
    start_ms : int
    end_ms : int

    