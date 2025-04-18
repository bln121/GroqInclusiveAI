import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
import requests
import uvicorn
from typing import List
import tempfile
from gtts import gTTS
from config import settings

# Import chat routes
from app.api.routes import chatRoutes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(
    title="Inclusive AI Backend",
    description="Backend API for Inclusive AI application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat routes
app.include_router(chatRoutes.router, prefix=settings.API_V1_STR)

# Create a static directory for video config if it doesn't exist
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_text: str

class LanguageListResponse(BaseModel):
    languages: List[str]

class SpeakRequest(BaseModel):
    text: str
    language: str = "en"

def translate_text(text: str, source_language: str, target_language: str) -> str:
    """
    Call the Groq API to translate text from source_language to target_language.
    Returns only the translated text.
    """
    if not text or not target_language:
        return "Please provide text and select a language."

    prompt = (
        f"Translate the following text from {source_language} to {target_language}. "
        f"Return only the translated text, with no additional explanation, transliteration, or formatting: {text}"
    )
    
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": settings.MAX_TOKENS,
        "temperature": settings.TEMPERATURE
    }
    
    try:
        response = requests.post(settings.GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        translated_text = result["choices"][0]["message"]["content"].strip()
        return translated_text
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post(f"{settings.API_V1_STR}/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Handle translation requests.
    """
    translated_text = translate_text(
        request.text,
        request.source_language,
        request.target_language
    )
    return {"translated_text": translated_text}

@app.post(f"{settings.API_V1_STR}/speak")
async def speak(request: SpeakRequest):
    """
    Generate speech audio for the given text using gTTS.
    """
    return await text_to_speech_handler(request)

@app.post(f"{settings.API_V1_STR}/text-to-speech")
async def text_to_speech(request: SpeakRequest):
    """
    Alternative endpoint for text-to-speech functionality.
    """
    return await text_to_speech_handler(request)

@app.post("/speak")
async def speak_legacy(request: SpeakRequest):
    """
    Legacy endpoint for speech generation.
    """
    return await text_to_speech_handler(request)

async def text_to_speech_handler(request: SpeakRequest):
    """
    Common handler for text-to-speech functionality.
    """
    text = request.text.strip()
    language = request.language
    
    if language in settings.LANGUAGE_CODES:
        language = settings.LANGUAGE_CODES[language]
    
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
        
        async def cleanup():
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                    logger.info(f"Cleaned up temporary file: {temp_file_path}")
                except Exception as e:
                    logger.error(f"Failed to clean up temporary file: {str(e)}")

        return FileResponse(
            temp_file_path,
            media_type="audio/mpeg",
            filename="output.mp3",
            background=cleanup
        )
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}")
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"Cleaned up temporary file on error: {temp_file_path}")
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}")

@app.get(f"{settings.API_V1_STR}/languages", response_model=LanguageListResponse)
async def get_languages():
    """
    Get list of supported languages.
    """
    return {"languages": settings.SUPPORTED_LANGUAGES}

@app.get("/")
async def root():
    return {
        "message": "Welcome to Inclusive AI Backend",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=True)
