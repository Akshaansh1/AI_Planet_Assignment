from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from ..core.database import Base

class Workflow(Base):
    """
    SQLAlchemy model for storing workflow definitions.
    """
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    definition = Column(JSONB)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())

