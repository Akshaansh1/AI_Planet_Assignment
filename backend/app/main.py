from fastapi import FastAPI
from .api import routes_document 
from .core.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Include routers
app.include_router(routes_document.router, prefix="/api/v1/documents", tags=["documents"])
# Include other routers here as you build them

@app.get("/")
def read_root():
    return {"message": "Welcome to the No-Code/Low-Code Workflow API"}

