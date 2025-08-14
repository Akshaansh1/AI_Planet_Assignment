from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services import chat_service
from .. import schemas
from typing import List

router = APIRouter()

@router.get("/history/{workflow_id}", response_model=List[schemas.chat_schema.ChatLog])
def get_chat_history(workflow_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the chat history for a specific workflow.
    """
    return chat_service.get_chat_logs_by_workflow(db, workflow_id=workflow_id)
