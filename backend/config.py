import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # API Settings
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Groq API Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_API_URL: str = os.getenv("GROQ_API_URL")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE"))
    
    # Chat Settings
    CHAT_MODEL: str = os.getenv("CHAT_MODEL")
    
    # CORS Settings
    ALLOW_ORIGINS: List[str] = os.getenv("ALLOW_ORIGINS", "*").split(",")
    
    # Gesture Recognition Settings
    GESTURE_CONFIDENCE_THRESHOLD: float = float(os.getenv("GESTURE_CONFIDENCE_THRESHOLD"))
    SWIPE_THRESHOLD: float = float(os.getenv("SWIPE_THRESHOLD"))
    
    # Supported Languages
    SUPPORTED_LANGUAGES: List[str] = ["English", "Hindi", "Telugu", "Kannada", "Tamil"]
    
    # Language Codes
    LANGUAGE_CODES: dict = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Kannada": "kn",
        "Tamil": "ta"
    }

# Create settings instance
settings = Settings()
