from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# Schemas for React Flow structure
class NodeData(BaseModel):
    label: str

class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: NodeData
    width: Optional[int] = None
    height: Optional[int] = None

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None

class WorkflowDefinition(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

# Schemas for Workflow model
class WorkflowBase(BaseModel):
    name: str
    definition: WorkflowDefinition

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(WorkflowBase):
    pass

class Workflow(WorkflowBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
