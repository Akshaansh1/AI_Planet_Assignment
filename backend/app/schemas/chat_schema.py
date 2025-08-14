from pydantic import BaseModel
from datetime import datetime

class ChatLogBase(BaseModel):
    workflow_id: int
    sender: str
    message: str

class ChatLogCreate(ChatLogBase):
    pass

class ChatLog(ChatLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
