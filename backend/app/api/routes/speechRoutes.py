from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
import tempfile
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class SpeakRequest(BaseModel):
    text: str
    language: str = "en"

@router.post("/text-to-speech")
async def text_to_speech(request: SpeakRequest):
    """
    Generate speech audio for the given text using gTTS.
    """
    text = request.text.strip()
    language = request.language
    
    if not text:
        logger.error("No text provided for speech generation")
        raise HTTPException(status_code=400, detail="No text provided")
    
    if language not in ['en', 'hi', 'te', 'kn', 'ta']:
        logger.warning(f"Unsupported language code: {language}")
        raise HTTPException(status_code=400, detail=f"Language '{language}' is not supported for speech")

    logger.info(f"Generating speech for text: '{text}' in language: {language}")
    
    temp_file_path = None
    try:
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file_path = temp_file.name
            tts.save(temp_file_path)
            logger.info(f"Audio saved to temporary file: {temp_file_path}")
        
        # Define cleanup callback
        async def cleanup():
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                    logger.info(f"Cleaned up temporary file: {temp_file_path}")
                except Exception as e:
                    logger.error(f"Failed to clean up temporary file: {str(e)}")

        # Return FileResponse with cleanup callback
        return FileResponse(
            temp_file_path,
            media_type="audio/mpeg",
            filename="output.mp3",
            background=cleanup
        )
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}")
        # Clean up if file was created
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"Cleaned up temporary file on error: {temp_file_path}")
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}") 