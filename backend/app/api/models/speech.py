from pydantic import BaseModel

class SpeechData(BaseModel):
    audio_data: str  # Base64 encoded audio
    language: str

class SpeechResponse(BaseModel):
    text: str
    language: str 