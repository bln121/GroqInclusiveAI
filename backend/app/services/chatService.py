import os
import json
import logging
import uuid
import io
import base64
from datetime import datetime
from typing import Dict, List, Optional, Any
from tempfile import NamedTemporaryFile
from gtts import gTTS
from groq import Groq
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from config import settings

# Ensure consistent language detection
DetectorFactory.seed = 0

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Language mappings for better detection
LANGUAGE_MAPPING = {
    'en': 'English',
    'hi': 'Hindi', 
    'te': 'Telugu',
    'kn': 'Kannada',
    'ta': 'Tamil'
}

class ChatService:
    def __init__(self):
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
        self.chat_storage_path = "chat_histories.json"
        self.chat_histories = self._load_chat_histories()
    
    def _load_chat_histories(self) -> Dict[str, Dict[str, Any]]:
        """Load chat histories from storage file"""
        if os.path.exists(self.chat_storage_path):
            try:
                with open(self.chat_storage_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Error decoding chat histories file: {self.chat_storage_path}")
                return {}
        return {}
    
    def _save_chat_histories(self) -> None:
        """Save chat histories to storage file"""
        with open(self.chat_storage_path, 'w') as f:
            json.dump(self.chat_histories, f)
    
    def get_chat_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all chat sessions with metadata"""
        return {
            sid: {"created": info["created"], "message_count": len(info["messages"])}
            for sid, info in self.chat_histories.items()
        }
    
    def get_chat_history(self, session_id: Optional[str] = None) -> tuple[str, List[Dict[str, Any]]]:
        """Get or create a chat session"""
        if not session_id or session_id not in self.chat_histories:
            session_id = str(uuid.uuid4())
            self.chat_histories[session_id] = {"messages": [], "created": datetime.now().isoformat()}
        return session_id, self.chat_histories[session_id]["messages"]
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the input text with improved accuracy"""
        try:
            # Check for specific patterns that might indicate a language more reliably
            if any(word in text.lower() for word in ['namaste', 'hindi', 'बात', 'नमस्ते', 'हिंदी']):
                logger.info("Hindi language detected based on specific patterns")
                return 'hi'
            
            if any(word in text.lower() for word in ['telugu', 'తెలుగు', 'నమస్కారం']):
                logger.info("Telugu language detected based on specific patterns")
                return 'te'
            
            # Try standard detection
            detected_language = detect(text)
            logger.info(f"Detected language: {detected_language}")
            
            # Map to supported languages or default to English
            if detected_language in ['en', 'hi', 'te', 'kn', 'ta']:
                return detected_language
            return "en"
        except LangDetectException:
            logger.warning("Language detection failed. Defaulting to English.")
            return "en"
    
    def get_language_name(self, lang_code: str) -> str:
        """Convert language code to language name"""
        return LANGUAGE_MAPPING.get(lang_code, "English")
    
    def generate_response(self, query: str, chat_history: List[Dict[str, Any]]) -> str:
        """Generate a response using the Groq API with language awareness"""
        detected_language = self.detect_language(query)
        language_name = self.get_language_name(detected_language)
        
        # Create a language-aware system prompt
        system_prompt = f"""You are a multilingual AI assistant capable of fluently communicating in multiple languages.
When users speak to you in a particular language, you MUST ALWAYS respond in that same language.
Currently, the user is communicating in {language_name}.
YOUR RESPONSE MUST BE ENTIRELY IN {language_name}.
Maintain a helpful, friendly, and professional tone in your responses."""
        
        # Create the user prompt
        user_prompt = f"""
User query: {query}
Previous context: {chat_history[-5:] if chat_history else []}

Remember to respond ONLY in {language_name}.
Current date: {datetime.now().strftime("%B %d, %Y")}
"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=settings.CHAT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )
            answer = response.choices[0].message.content.strip()
            
            # Check if response is in correct language (basic check)
            response_language = self.detect_language(answer)
            if response_language != detected_language:
                logger.warning(f"Response language mismatch: expected {detected_language}, got {response_language}")
                # For safety, add a note in the detected language
                if detected_language == 'hi':
                    answer = f"मुझे खेद है, मैं अपना उत्तर हिंदी में देने में असमर्थ था। {answer}"
                elif detected_language == 'te':
                    answer = f"క్షమించండి, నేను తెలుగులో సమాధానం ఇవ్వలేకపోయాను. {answer}"
                
            return answer
        except Exception as e:
            logger.error(f"Error with Groq API: {str(e)}")
            raise Exception(f"Error processing query with AI: {str(e)}")
    
    def process_text_query(self, query: str, session_id: Optional[str] = None, output_as_voice: bool = False) -> Dict[str, Any]:
        """Process a text query and return the response"""
        # Check for inappropriate content
        if any(word in query.lower() for word in ["hate", "kill", "death", "violence"]):
            if "deserve" in query.lower() and "death" in query.lower():
                return {"text_response": "As an AI, I am not allowed to make choices about who deserves the death penalty."}
            return {"text_response": "Sorry, I cannot assist with inappropriate or harmful content."}
        
        # Get or create a chat session
        session_id, chat_history = self.get_chat_history(session_id)
        
        # If just loading history
        if query.lower().strip() == "load history":
            return {"text_response": "", "session_id": session_id, "chat_history": chat_history}
        
        # Generate response
        answer = self.generate_response(query, chat_history)
        
        # Update chat history
        current_time = datetime.now().strftime("%H:%M")
        chat_history.append({"role": "user", "content": query, "time": current_time})
        chat_history.append({"role": "assistant", "content": answer, "time": current_time})
        self._save_chat_histories()
        
        # Prepare response
        response_data = {
            "text_response": answer,
            "session_id": session_id,
            "chat_history": chat_history
        }
        
        # Generate audio if requested
        if output_as_voice:
            detected_language = self.detect_language(answer)
            lang_code = detected_language if detected_language in ["te", "hi", "en"] else "en"
            
            try:
                tts = gTTS(text=answer, lang=lang_code)
                with io.BytesIO() as audio_buffer:
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    response_data["audio_response"] = base64.b64encode(audio_buffer.read()).decode('utf-8')
            except Exception as e:
                logger.error(f"TTS error: {str(e)}")
                response_data["audio_response"] = None
        
        return response_data
    
    def edit_message(self, session_id: str, message_index: int, new_content: str) -> Dict[str, Any]:
        """Edit a message in the chat history"""
        if session_id not in self.chat_histories:
            raise ValueError("Session not found")
            
        chat_history = self.chat_histories[session_id]["messages"]
        if 0 <= message_index < len(chat_history):
            chat_history[message_index]["content"] = new_content
            chat_history[message_index]["time"] = datetime.now().strftime("%H:%M")
            self._save_chat_histories()
            return {"status": "success", "chat_history": chat_history}
        else:
            raise ValueError("Invalid message index")
            
    def delete_chat_session(self, session_id: str) -> Dict[str, Any]:
        """Delete a chat session"""
        if session_id not in self.chat_histories:
            raise ValueError("Session not found")
            
        # Remove the session from chat histories
        del self.chat_histories[session_id]
        
        # Save changes
        self._save_chat_histories()
        
        return {"status": "success"}
