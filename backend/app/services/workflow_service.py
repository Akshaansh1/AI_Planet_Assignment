from sqlalchemy.orm import Session
from .. import models
from ..schemas import workflow_schema


class WorkflowService:
    """
    Service for handling workflow-related operations.
    """

    def get_workflow(self, db: Session, workflow_id: int):
        return (
            db.query(models.workflow.Workflow)
            .filter(models.workflow.Workflow.id == workflow_id)
            .first()
        )

    def get_workflows(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.workflow.Workflow).offset(skip).limit(limit).all()

    def create_workflow(
        self, db: Session, workflow: workflow_schema.WorkflowCreate
    ):  # Corrected usage
        # workflow.definition may be a plain dict (from frontend JSON) or a Pydantic object.
        definition_value = workflow.definition
        try:
            # pydantic v2 model -> model_dump
            if hasattr(workflow.definition, "model_dump"):
                definition_value = workflow.definition.model_dump()
            # pydantic v1 -> dict()
            elif hasattr(workflow.definition, "dict"):
                definition_value = workflow.definition.dict()
        except Exception:
            # fallback: use as-is
            definition_value = workflow.definition

        db_workflow = models.workflow.Workflow(
            name=workflow.name, definition=definition_value
        )
        db.add(db_workflow)
        db.commit()
        db.refresh(db_workflow)
        return db_workflow

    def update_workflow(
        self, db: Session, workflow_id: int, workflow: workflow_schema.WorkflowUpdate
    ):
        db_workflow = self.get_workflow(db, workflow_id)
        if db_workflow:
            update_data = workflow.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_workflow, key, value)
            db.commit()
            db.refresh(db_workflow)
        return db_workflow

    def delete_workflow(self, db: Session, workflow_id: int):
        db_workflow = self.get_workflow(db, workflow_id)
        if db_workflow:
            db.delete(db_workflow)
            db.commit()
        return db_workflow


workflow_service = WorkflowService()
