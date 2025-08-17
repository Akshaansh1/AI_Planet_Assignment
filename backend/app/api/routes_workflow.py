from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..core.database import get_db
from ..services import workflow_service, chat_service
from ..utils.workflow_executor import workflow_executor
from .. import schemas
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.workflow_schema.Workflow)
def create_workflow(workflow: schemas.workflow_schema.WorkflowCreate, db: Session = Depends(get_db)):
    return workflow_service.create_workflow(db=db, workflow=workflow)

@router.get("/", response_model=List[schemas.workflow_schema.Workflow])
def read_workflows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workflows = workflow_service.get_workflows(db, skip=skip, limit=limit)
    return workflows

@router.get("/{workflow_id}", response_model=schemas.workflow_schema.Workflow)
def read_workflow(workflow_id: int, db: Session = Depends(get_db)):
    db_workflow = workflow_service.get_workflow(db, workflow_id=workflow_id)
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_workflow

@router.put("/{workflow_id}", response_model=schemas.workflow_schema.Workflow)
def update_workflow(workflow_id: int, workflow: schemas.workflow_schema.WorkflowUpdate, db: Session = Depends(get_db)):
    return workflow_service.update_workflow(db=db, workflow_id=workflow_id, workflow=workflow)

@router.delete("/{workflow_id}", response_model=schemas.workflow_schema.Workflow)
def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
    return workflow_service.delete_workflow(db=db, workflow_id=workflow_id)

class QueryRequest(BaseModel):
    query: str

@router.post("/{workflow_id}/execute")
def execute_workflow(workflow_id: int, request: QueryRequest, db: Session = Depends(get_db)):
    """
    Executes a defined workflow with a user query.
    """
    db_workflow = workflow_service.get_workflow(db, workflow_id=workflow_id)
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Log user query (ensure string)
    user_msg = request.query if request.query is not None else ""
    chat_service.create_chat_log(
        db,
        schemas.chat_schema.ChatLogCreate(
            workflow_id=workflow_id, sender="user", message=str(user_msg)
        ),
    )

    # Execute the workflow
    result = workflow_executor.execute(db_workflow.definition, request.query)

    # Determine bot message safely (avoid passing None to pydantic)
    bot_msg = None
    if isinstance(result, dict):
        if "response" in result and result.get("response") is not None:
            bot_msg = result.get("response")
        elif "error" in result and result.get("error") is not None:
            bot_msg = str(result.get("error"))
        else:
            bot_msg = str(result)
    else:
        bot_msg = str(result)

    # Log bot response (always log a string)
    try:
        chat_service.create_chat_log(
            db,
            schemas.chat_schema.ChatLogCreate(
                workflow_id=workflow_id, sender="bot", message=str(bot_msg)
            ),
        )
    except Exception:
        # If logging fails, continue and return the result; avoid raising a 500 for logging issues
        pass

    return result
