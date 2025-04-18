from gtts import gTTS
import speech_recognition as sr
import os
from typing import Optional
import tempfile
from ..config import settings

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.languageCodes = settings.LANGUAGE_CODES

    def textToSpeech(self, text: str, language: str) -> Optional[str]:
        """Convert text to speech and return the path to the audio file."""
        try:
            # Get language code
            langCode = self.languageCodes.get(language, "en")
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tempFile:
                tempPath = tempFile.name
            
            # Generate speech
            tts = gTTS(text=text, lang=langCode, slow=False)
            tts.save(tempPath)
            
            return tempPath
        except Exception as e:
            print(f"Error in text-to-speech conversion: {str(e)}")
            return None

    def speechToText(self, audioData: bytes, language: str) -> Optional[str]:
        """Convert speech to text."""
        try:
            # Get language code
            langCode = self.languageCodes.get(language, "en")
            
            # Create a temporary file for the audio data
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tempFile:
                tempFile.write(audioData)
                tempPath = tempFile.name
            
            # Process the audio file
            with sr.AudioFile(tempPath) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=langCode)
            
            # Clean up
            os.unlink(tempPath)
            
            return text
        except Exception as e:
            print(f"Error in speech-to-text conversion: {str(e)}")
            return None 