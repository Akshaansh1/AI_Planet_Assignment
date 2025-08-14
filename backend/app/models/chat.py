from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class ChatLog(Base):
    """
    SQLAlchemy model for storing chat logs.
    """
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    sender = Column(String) 
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    workflow = relationship("Workflow")
