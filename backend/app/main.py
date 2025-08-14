from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="AI Planet API",
    description="No-Code/Low-Code Workflow API with AI capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers with error handling
try:
    from .api.routes_document import router as document_router
    app.include_router(document_router, prefix="/api/v1/documents", tags=["documents"])
    logger.info("✓ Document routes loaded successfully")
except ImportError as e:
    logger.warning(f"⚠ Warning: Could not load document routes: {e}")

try:
    from .api.routes_chat import router as chat_router
    app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
    logger.info("✓ Chat routes loaded successfully")
except ImportError as e:
    logger.warning(f"⚠ Warning: Could not load chat routes: {e}")

try:
    from .api.routes_knowledge_base import router as kb_router
    app.include_router(kb_router, prefix="/api/v1/knowledge", tags=["knowledge"])
    logger.info("✓ Knowledge base routes loaded successfully")
except ImportError as e:
    logger.warning(f"⚠ Warning: Could not load knowledge base routes: {e}")

try:
    from .api.routes_llm_engine import router as llm_router
    app.include_router(llm_router, prefix="/api/v1/llm", tags=["llm"])
    logger.info("✓ LLM engine routes loaded successfully")
except ImportError as e:
    logger.warning(f"⚠ Warning: Could not load LLM engine routes: {e}")

try:
    from .api.routes_workflow import router as workflow_router
    app.include_router(workflow_router, prefix="/api/v1/workflow", tags=["workflow"])
    logger.info("✓ Workflow routes loaded successfully")
except ImportError as e:
    logger.warning(f"⚠ Warning: Could not load workflow routes: {e}")

# Database initialization with error handling
try:
    from .core.database import engine, Base, test_connection
    if engine is not None:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created successfully")
        
        # Test connection
        if test_connection():
            logger.info("✓ Database connection test successful")
        else:
            logger.warning("⚠ Database connection test failed")
    else:
        logger.warning("⚠ Database engine not available")
except Exception as e:
    logger.warning(f"⚠ Warning: Could not initialize database: {e}")
    logger.info("   Make sure PostgreSQL is running and credentials are correct")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to AI Planet API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "message": "API is running",
        "database": "unknown",
        "chromadb": "unknown"
    }
    
    # Check database status
    try:
        from .core.database import test_connection
        if test_connection():
            health_status["database"] = "connected"
        else:
            health_status["database"] = "disconnected"
    except:
        health_status["database"] = "error"
    
    # Check ChromaDB status
    try:
        from .core.chroma import chroma_client
        if chroma_client and chroma_client.is_connected():
            health_status["chromadb"] = "connected"
        else:
            health_status["chromadb"] = "disconnected"
    except:
        health_status["chromadb"] = "error"
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Planet API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

