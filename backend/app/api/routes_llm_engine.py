from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..core.database import get_db
from ..services import workflow_service
from ..utils.workflow_executor import workflow_executor
from ..services import chat_service
from .. import schemas

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/workflow/{workflow_id}/execute")
def execute_workflow(workflow_id: int, request: QueryRequest, db: Session = Depends(get_db)):
    """
    Executes a defined workflow with a user query.
    """
    db_workflow = workflow_service.get_workflow(db, workflow_id=workflow_id)
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Log user query
    chat_service.create_chat_log(db, schemas.chat_schema.ChatLogCreate(
        workflow_id=workflow_id, sender="user", message=request.query
    ))

    # Execute the workflow
    result = workflow_executor.execute(db_workflow.definition, request.query)

    # Log bot response
    if "response" in result:
        chat_service.create_chat_log(db, schemas.chat_schema.ChatLogCreate(
            workflow_id=workflow_id, sender="bot", message=result["response"]
        ))

    return result
