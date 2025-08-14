from sqlalchemy.orm import Session
from .. import models, schemas
from ..core.embeddings import embedding_client
from ..core.chroma import chroma_client
from ..utils.pdf_parser import parse_pdf
import os
import logging

logger = logging.getLogger(__name__)

class DocumentService:
    """
    Service for handling document-related operations.
    """
    def get_document(self, db: Session, document_id: int):
        return db.query(models.document.Document).filter(models.document.Document.id == document_id).first()

    def get_documents(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.document.Document).offset(skip).limit(limit).all()

    def create_document(self, db: Session, file_path: str, filename: str):
        """
        Processes a document, stores its content and embeddings.
        """
        try:
            # 1. Parse the PDF
            content = parse_pdf(file_path)

            # 2. Store document metadata in PostgreSQL
            db_document = models.document.Document(filename=filename, content=content)
            db.add(db_document)
            db.commit()
            db.refresh(db_document)

            # 3. Generate embeddings (only if embedding client is available)
            try:
                if embedding_client:
                    openai_embedding = embedding_client.get_openai_embedding(content)
                    
                    # 4. Store in ChromaDB (only if available)
                    if chroma_client and chroma_client.is_connected():
                        collection = chroma_client.get_or_create_collection(name="documents")
                        if collection:
                            collection.add(
                                embeddings=[openai_embedding],
                                documents=[content],
                                metadatas=[{"filename": filename, "source": "openai", "doc_id": db_document.id}],
                                ids=[str(db_document.id)]
                            )
                            logger.info(f"Document {filename} stored in ChromaDB successfully")
                        else:
                            logger.warning("ChromaDB collection not available, skipping vector storage")
                    else:
                        logger.warning("ChromaDB not available, skipping vector storage")
                else:
                    logger.warning("Embedding client not available, skipping vector storage")
            except Exception as e:
                logger.error(f"Error processing embeddings or vector storage: {e}")
                # Continue without vector storage - document is still saved in PostgreSQL

            # Clean up the uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)

            return db_document
            
        except Exception as e:
            logger.error(f"Error creating document {filename}: {e}")
            # Clean up the uploaded file on error
            if os.path.exists(file_path):
                os.remove(file_path)
            raise e

document_service = DocumentService()
