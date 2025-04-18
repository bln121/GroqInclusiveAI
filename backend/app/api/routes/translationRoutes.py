from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import logging
from typing import List
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

router = APIRouter()

# Groq API configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY');
GROQ_API_URL = os.getenv('GROQ_API_URL');

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_text: str

class LanguageListResponse(BaseModel):
    languages: List[str]

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
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": GROQ_MODEL,  # Ensure this is properly loaded from environment or hardcoded
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        # Check if the API response contains the expected data structure
        if "choices" not in result or not result["choices"]:
            logger.error(f"Invalid response structure from Groq API: {result}")
            raise HTTPException(status_code=500, detail="Unexpected response format from Groq API")
        
        translated_text = result["choices"][0]["message"]["content"].strip()
        return translated_text
    except requests.RequestException as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
    except ValueError as e:
        logger.error(f"Error parsing response from Groq API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing translation: {str(e)}")

@router.post("/translate", response_model=TranslationResponse)
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

@router.get("/languages", response_model=LanguageListResponse)
async def get_languages():
    """
    Get list of supported languages.
    """
    languages = ["English", "Hindi", "Telugu", "Kannada", "Tamil"]
    return {"languages": languages} 