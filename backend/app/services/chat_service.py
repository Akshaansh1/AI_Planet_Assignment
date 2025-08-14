from sqlalchemy.orm import Session
from .. import models
from ..schemas import chat_schema

class ChatService:
    """
    Service for handling chat log operations.
    """
    def get_chat_logs_by_workflow(self, db: Session, workflow_id: int, skip: int = 0, limit: int = 100):
        return db.query(models.chat.ChatLog).filter(models.chat.ChatLog.workflow_id == workflow_id).offset(skip).limit(limit).all()

    def create_chat_log(self, db: Session, chat_log: chat_schema.ChatLogCreate): # Corrected usage
        db_chat_log = models.chat.ChatLog(**chat_log.dict())
        db.add(db_chat_log)
        db.commit()
        db.refresh(db_chat_log)
        return db_chat_log

chat_service = ChatService()
