from pydantic import BaseModel
from typing import Dict, Any

class ToolCallCreate(BaseModel):

    tool_name : str
    args : Dict[str, Any]
    results : Dict[str, Any]
    latency_ms : int
    success : bool
    