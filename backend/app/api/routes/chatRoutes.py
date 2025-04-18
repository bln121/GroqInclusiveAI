from fastapi import APIRouter, HTTPException, Request
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import logging
from config import settings
from ...services.chatService import ChatService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(tags=["chat"])

# Initialize chat service
chat_service = ChatService()

# Request models
class TextRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    output_as_voice: bool = False

class EditRequest(BaseModel):
    session_id: str
    message_index: int
    new_content: str

class DeleteSessionRequest(BaseModel):
    session_id: str

@router.get("/chat-sessions/")
async def get_chat_sessions():
    """Get all chat sessions"""
    return {
        "sessions": chat_service.get_chat_sessions()
    }

@router.post("/text-query/")
async def text_query(request: TextRequest):
    """Process a text query and return response"""
    try:
        logger.info(f"Received text query: {request.query}")
        response_data = chat_service.process_text_query(
            query=request.query,
            session_id=request.session_id,
            output_as_voice=request.output_as_voice
        )
        return response_data
    except Exception as e:
        logger.error(f"Error processing text query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/edit-message/")
async def edit_message(request: EditRequest):
    """Edit a message in chat history"""
    try:
        logger.info(f"Edit request: {request.dict()}")
        return chat_service.edit_message(
            session_id=request.session_id,
            message_index=request.message_index,
            new_content=request.new_content
        )
    except ValueError as e:
        logger.error(f"Edit error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Edit error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error editing message: {str(e)}")

@router.post("/voice-query/")
async def voice_query(request: TextRequest):
    """Process a voice query"""
    # For now, this routes to the same endpoint as text_query
    # with output_as_voice set to True
    request.output_as_voice = True
    return await text_query(request)

@router.delete("/chat-session/")
async def delete_chat_session(request: DeleteSessionRequest):
    """Delete a chat session"""
    try:
        logger.info(f"Delete session request: {request.session_id}")
        result = chat_service.delete_chat_session(session_id=request.session_id)
        return {"status": "success", "message": "Chat session deleted successfully"}
    except ValueError as e:
        logger.error(f"Delete error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")
