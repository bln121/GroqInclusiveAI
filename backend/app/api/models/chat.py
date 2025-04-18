from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    message: str
    language: str

class ChatResponse(BaseModel):
    response: str
    language: str

class LanguageList(BaseModel):
    languages: list[str] 