# Inclusive AI Backend

This is the backend service for the Inclusive AI application, providing APIs for:
- Multilingual chatbot
- Speech-to-text conversion
- Text-to-speech conversion

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the FastAPI server:
```bash
python run.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### Chat
- `POST /api/chat`
  - Request body: `{"message": "Hello", "language": "English"}`
  - Response: `{"response": "Hello! How can I help you today?"}`
  
### Speech Processing
- `POST /api/speech-to-text`
  - Request body: `{"audio_data": "base64_encoded_audio", "language": "English"}`
  - Response: `{"text": "Recognized text"}`

- `POST /api/text-to-speech`
  - Query params: `text=Hello&language=English`
  - Response: Audio file (MP3)

### Languages
- `GET /api/languages`
  - Response: `{"chat": ["English", "Telugu", "Hindi"], "speech": ["English", "Telugu", "Hindi"]}`

## Supported Languages

- English (en)
- Telugu (te)
- Hindi (hi)

## Development

The backend is built using:
- FastAPI for the web framework
- MediaPipe for gesture recognition
- gTTS for text-to-speech
- SpeechRecognition for speech-to-text

## Testing

To test the APIs, you can use tools like Postman or curl. Example:

```bash
# Test chat API
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "language": "English"}'
```

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 400: Bad Request
- 500: Internal Server Error

Error responses include a detail message explaining the issue. 