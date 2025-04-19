![github-submission-banner](https://github.com/bln121/GroqInclusiveAI)

# 🚀 Project Title

> A one-line tagline or mission statement for your project.

Multilingual AI Communication Assistant using Groq

---

## 📌 Problem Statement

Select the problem statement number and title from the official list given in Participant Manual.

**Example:**  
**Problem Statement 1 – Weave AI magic with Groq**

---

## 🎯 Objective

Build a creative and interactive multimodal application powered by Groq, leveraging its capabilities to 
solve real-world problems with a focus on user experience and innovation.

---

## 🧠 Team & Approach

### Team Name:  
`CodeCrafters`

### Team Members:  
- Penjuri Ganesh
- Sanka Dileep
- Chandravathi Kodudhula
- Bachu Lakshmi Narayana
*(Add links if you want)*(GitHub / LinkedIn / Role)  

### Your Approach:  
- Why you choose this problem  
    We selected this problem because India’s linguistic diversity and the needs of sensory-impaired individuals highlight a critical gap in accessible digital communication. We wanted to leverage Groq’s advanced AI capabilities to create an inclusive solution that empowers diverse users, aligning with our passion for innovation and social impact.
- Key challenges you addressed  
    1. Developing a system that supports real-time multilingual speech-to-text, speech-to-speech, text-to-text and text-to-speech conversion in English, Telugu, Tamil, Kannada and Hindi, ensuring accuracy across    diverse accents and dialects.
    2. Designing an accessible AI chatbot that caters to sensory-impaired users, requiring robust integration of text and audio modalities powered by Groq.
    3. Ensuring a seamless user experience (UX) with high design quality, addressing the complexity of handling multiple modalities (text, audio) effectively.
- Any pivots, brainstorms, or breakthroughs during hacking  
    1. Initially, we brainstormed a broader language set but pivoted to focus on English, Telugu, Tamil,Kannada and Hindi to prioritize depth and performance within the hackathon timeframe.
    2. A breakthrough came when we discovered Groq's ability to handle audio processing, enabling us to integrate real-time voice interaction, significantly enhancing accessibility for visually impaired users.
    3. We held multiple brainstorming sessions to refine the chatbot's context-aware responses, leading to a pivot from generic replies to tailored solutions for sensory-impaired users, improving overall usability.
---

## 🛠️ Tech Stack

### Core Technologies Used:
- Frontend: React.js and Bootstrap
- Backend: Python and FastAPI
- APIs: Groq
- Hosting: AWS

### Sponsor Technologies Used (if any):
- [✅] **Groq:**:
    Groq was utilized as the core AI engine to power the multilingual text translation feature. The application leverages Groq's API (via the llama3-70b-8192 model) to translate text between languages such as English, Hindi, Telugu, Kannada, and Tamil. The translation process is integrated into a FastAPI backend, where Groq processes user input and returns translated text in real-time, enhancing the application's ability to address communication barriers in diverse linguistic contexts.
- [ ] **Monad:** _Your blockchain implementation_  
- [ ] **Fluvio:** _Real-time data handling_  
- [ ] **Base:** _AgentKit / OnchainKit / Smart Wallet usage_  
- [ ] **Screenpipe:** _Screen-based analytics or workflows_  
- [ ] **Stellar:** _Payments, identity, or token usage_
*(Mark with ✅ if completed)*
---

## ✨ Key Features

Highlight the most important features of your project:

- ✅ Feature 1  Multilingual Translator
- ✅ Feature 2  Multilingual Groq AI Chatbot


Add images, GIFs, or screenshots if helpful!

---

## 📽️ Demo & Deliverables

- **Demo Video Link:** [https://drive.google.com/file/d/1y_r-1-RCYKYupzHBTaGbYKVsNskSC5B_/view?usp=drive_link]  
- **Pitch Deck / PPT Link:** [https://docs.google.com/presentation/d/1wA0u2vMKs-yP_jgZyo__GuFzVM-L66jk/edit?usp=drivesdk&ouid=111919240505857663062&rtpof=true&sd=true]  

---

## ✅ Tasks & Bonus Checklist

- [✅] **All members of the team completed the mandatory task - Followed at least 2 of our social channels and filled the form** (Details in Participant Manual)  
- [✅] **All members of the team completed Bonus Task 1 - Sharing of Badges and filled the form (2 points)**  (Details in Participant Manual)
- [✅] **All members of the team completed Bonus Task 2 - Signing up for Sprint.dev and filled the form (3 points)**  (Details in Participant Manual)

*(Mark with ✅ if completed)*

---

## 🧪 How to Run the Project

### Requirements:
- Node.js (v16 or higher) for the frontend
- Python (v3.8 or higher) for the backend
- API Keys:
    Groq API key for translation (set in backend .env file)
- .env file setup:
    Frontend: Not required.
    Backend: Create a .env file in the backend root directory with the following:
        GROQ_API_KEY=your_groq_api_key
        GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
        GROQ_MODEL=llama3-8b-8192
        MAX_TOKENS=1024
        TEMPERATURE=0.7
        ALLOW_ORIGINS=http://localhost:3000
        API_V1_STR=/api/v1
        HOST=0.0.0.0
        PORT=8000
        SUPPORTED_LANGUAGES=en,hi,te,kn,ta
        LANGUAGE_CODES={"en": "en", "hi": "hi", "te": "te", "kn": "kn", "ta": "ta"}

### Local Setup:
```bash
# Clone the repo
git clone https://github.com/your-team/inclusive-ai
# Navigate to the project directory
cd inclusive-ai

# Frontend setup
# Navigate to the frontend directory (if separate, assuming root here)
cd frontend
# Install dependencies
npm install
# Start the development server
npm start
# The frontend will run on http://localhost:3000 by default.
# Ensure the backend is running to handle API requests.

#Backend setup
# Navigate to the backend directory (if separate, assuming root here)
cd backend
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn requests gtts pydantic python-dotenv

# Start the backend server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Provide any backend/frontend split or environment setup notes here.

---

## 🧬 Future Scope

List improvements, extensions, or follow-up features:

- 📈 More integrations  
    Adding support for additional translation APIs (e.g., DeepL, Google Translate) for redundancy and improved accuracy.
    Integration of real-time speech recognition for enhanced speech-to-text functionality.
    Incorporate a database (e.g., PostgreSQL) to store user preferences and translation history.
- 🛡️ Security enhancements  
    Implementation of user authentication (e.g., OAuth2 or JWT) to secure API endpoints.
    Adding of rate limiting to prevent abuse of translation and speech endpoints.
    Validation and sanitize user inputs to prevent injection attacks.
- 🌐 Localization / broader accessibility  
    Expansion of supported languages beyond en, hi, te, kn, ta to include more global and regional languages.
    Improving accessibility with ARIA labels and screen reader support in the frontend.
    Adding right-to-left (RTL) language support for languages like Arabic and Hebrew.
    Optimization of text-to-speech for natural-sounding voices and additional accents.
---

## 📎 Resources / Credits

- APIs or datasets used :
    Groq API: Powers the translation functionality, enabling multilingual text processing.
    gTTS (Google Text-to-Speech): Used for generating audio from text in supported languages.
- Open source libraries or tools referenced  
    Frontend:
        React: JavaScript library for building user interfaces.
        React Router: Handles client-side routing.
        Bootstrap: CSS framework for responsive styling.
        Create React App: Boilerplate for setting up the React project.

    Backend:
        FastAPI: High-performance web framework for building APIs.
        Uvicorn: ASGI server for running FastAPI.
        gTTS: Python library for text-to-speech conversion.
        Pydantic: Data validation and settings management.
        python-dotenv: Loads environment variables from .env files.
        Requests: HTTP library for making API calls.
- Acknowledgements  
    Thanks to the xAI team for providing the Groq API, which made seamless translation possible.
    Gratitude to the open-source community for maintaining robust libraries like FastAPI, React, and gTTS.
    Special shout-out to the hackathon organizers for creating an inspiring environment to build this project.
---

## 🏁 Final Words

Share your hackathon journey — challenges, learnings, fun moments, or shout-outs!

    Our hackathon journey was a whirlwind of creativity, collaboration, and caffeine! Building this multilingual AI application was both challenging and rewarding. We faced hurdles like configuring CORS for seamless frontend-backend communication and ensuring gTTS supported our target languages, but each obstacle taught us something new. The thrill of seeing the first successful translation and hearing the text-to-speech output was unforgettable!

    Key learnings included mastering FastAPI's async capabilities and optimizing React's lazy loading for performance. The fun moments? Late-night debugging sessions turned into laugh-fests, and we celebrated small wins with virtual high-fives. A huge shout-out to our team for their relentless energy, the hackathon organizers for an amazing platform, and the open-source community for tools that made this possible. We're excited to see where this project goes next!

---
