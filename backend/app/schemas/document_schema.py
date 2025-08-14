from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
