from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Dict
import json

class Settings(BaseSettings):
    # API & Server
    API_V1_STR: str
    PROJECT_NAME: str
    HOST: str
    PORT: int

    # Groq API
    GROQ_API_KEY: str
    GROQ_API_URL: str
    GROQ_MODEL: str
    MAX_TOKENS: int
    TEMPERATURE: float

    # Chat
    CHAT_MODEL: str

    # CORS
    CORS_ORIGINS: List[str] = Field(default_factory=list)

    # Gesture
    GESTURE_CONFIDENCE_THRESHOLD: float
    SWIPE_THRESHOLD: float

    # Language
    SUPPORTED_LANGUAGES: List[str] = Field(default_factory=list)
    LANGUAGE_CODES: Dict[str, str] = Field(default_factory=dict)

    class Config:
        case_sensitive = True

    def __init__(self, **values):
        # Parse comma-separated strings and JSON strings
        if 'CORS_ORIGINS' in values and isinstance(values['CORS_ORIGINS'], str):
            values['CORS_ORIGINS'] = values['CORS_ORIGINS'].split(',')

        if 'SUPPORTED_LANGUAGES' in values and isinstance(values['SUPPORTED_LANGUAGES'], str):
            values['SUPPORTED_LANGUAGES'] = values['SUPPORTED_LANGUAGES'].split(',')

        if 'LANGUAGE_CODES' in values and isinstance(values['LANGUAGE_CODES'], str):
            values['LANGUAGE_CODES'] = json.loads(values['LANGUAGE_CODES'])

        super().__init__(**values)

# Create instance
settings = Settings()