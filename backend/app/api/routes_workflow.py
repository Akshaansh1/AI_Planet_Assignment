from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services import workflow_service
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
