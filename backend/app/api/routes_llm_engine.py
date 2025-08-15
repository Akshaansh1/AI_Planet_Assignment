from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging
import traceback
from ..core.database import get_db
from ..services import workflow_service
from ..utils.workflow_executor import workflow_executor
from ..services import chat_service
from .. import schemas
from ..core.config import settings
from ..core.llm_client import get_mistral_response

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.get("/api-key-status")
async def get_api_key_status():
    """
    Check if API keys are configured for different providers.
    Returns only boolean status, not the actual keys.
    """
    # Add logging to debug
    print("Mistral key present:", bool(settings.MISTRAL_API_KEY))
    print(
        "Mistral key length:",
        len(settings.MISTRAL_API_KEY) if settings.MISTRAL_API_KEY else 0,
    )

    return {
        "mistral": bool(settings.MISTRAL_API_KEY),
    }


@router.post("/test-api-key/{provider}")
async def test_api_key(provider: str):
    """
    Test if the API key works by making a simple test request.
    """
    try:
        test_prompt = (
            "Please respond with 'Hello!' to confirm the API connection is working."
        )
        # Only Mistral is supported. Map legacy provider names to mistral for UX convenience.
        if provider not in {"mistral", "openai", "gemini"}:
            raise HTTPException(
                status_code=400, detail="Invalid provider. Use 'mistral'."
            )

        response = await get_mistral_response(test_prompt, "mistral-small", 0.7)
        if response:
            return {"status": "success", "provider": "Mistral", "message": response}
    except Exception as e:
        print(f"Test API key error for {provider}: {type(e).__name__} - {str(e)}")
        if isinstance(e, RuntimeError):
            raise HTTPException(status_code=400, detail=str(e))
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Error testing {provider} API: {type(e).__name__} - {str(e)}",
            )


@router.post("/workflow/{workflow_id}/execute")
def execute_workflow(
    workflow_id: int, request: QueryRequest, db: Session = Depends(get_db)
):
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
