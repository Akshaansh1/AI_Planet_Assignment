from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services import document_service
from ..schemas import document_schema
import shutil
from typing import List

router = APIRouter()

@router.post("/upload", response_model= document_schema.Document)
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint to upload a document, process it, and store it.
    """
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = document_service.create_document(db, temp_file_path, file.filename)
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if file:
            file.file.close()

@router.get("/{document_id}", response_model= document_schema.Document)
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_document = document_service.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@router.get("/", response_model=List[ document_schema.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = document_service.get_documents(db, skip=skip, limit=limit)
    return documents
