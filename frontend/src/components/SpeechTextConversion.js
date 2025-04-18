import React, { useState, useRef, useEffect } from 'react';
import '../styles/SpeechTextConversion.css';

function SpeechTextConversion() {
    const [inputText, setInputText] = useState('');
    const [translatedText, setTranslatedText] = useState('');
    const [sourceLanguage, setSourceLanguage] = useState('English');
    const [targetLanguage, setTargetLanguage] = useState('English');
    const [status, setStatus] = useState('');
    const [speechStatus, setSpeechStatus] = useState('');
    const [isListening, setIsListening] = useState(false);
    const [isTranslating, setIsTranslating] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const recognitionRef = useRef(null);

    const languages = ['English', 'Telugu', 'Hindi', 'Kannada', 'Tamil'];
    const languageCodes = {
        'English': 'en',
        'Telugu': 'te',
        'Hindi': 'hi',
        'Kannada': 'kn',
        'Tamil': 'ta'
    };

    const handleVoiceInput = () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (SpeechRecognition) {
            // If already listening, stop
            if (isListening) {
                if (recognitionRef.current) {
                    recognitionRef.current.stop();
                }
                setIsListening(false);
                return;
            }

            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = false;
            recognitionRef.current.interimResults = false;
            recognitionRef.current.lang = languageCodes[sourceLanguage] + '-IN';

            recognitionRef.current.onstart = () => {
                setIsListening(true);
                setStatus('Listening...');
            };

            recognitionRef.current.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                setInputText(transcript);
                setStatus('Speech recognized successfully.');
            };

            recognitionRef.current.onerror = (event) => {
                setStatus(`Error during speech recognition: ${event.error}`);
                setIsListening(false);
            };

            recognitionRef.current.onend = () => {
                if (status === 'Listening...') {
                    setStatus('Speech recognition stopped.');
                }
                setIsListening(false);
            };

            recognitionRef.current.start();
        } else {
            setStatus('Speech recognition not supported in this browser.');
        }
    };

    const handleSpeakOutput = async () => {
        if (!translatedText || translatedText.startsWith('Error')) {
            setSpeechStatus('No valid text to speak.');
            return;
        }

        try {
            const languageCode = languageCodes[targetLanguage];

            if (!languageCode) {
                setSpeechStatus('Speech synthesis for this language is not supported.');
                return;
            }

            setIsSpeaking(true);
            setSpeechStatus(`Generating ${targetLanguage} speech...`);
            
            const response = await fetch(`/api/v1/text-to-speech`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    text: translatedText, 
                    language: languageCode 
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to generate speech');
            }

            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            
            setSpeechStatus(`Playing ${targetLanguage} speech...`);
            audio.play();
            
            audio.onended = () => {
                setSpeechStatus(`Finished playing ${targetLanguage} speech.`);
                setIsSpeaking(false);
            };
        } catch (error) {
            setSpeechStatus(`Error generating ${targetLanguage} speech: ${error.message}`);
            setIsSpeaking(false);
        }
    };

    const handleTranslate = async (e) => {
        e.preventDefault();
        if (!inputText.trim()) {
            setStatus('Please enter some text to translate.');
            return;
        }
        
        try {
            setIsTranslating(true);
            setTranslatedText('');
            
            const response = await fetch(`/api/v1/translate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: inputText,
                    source_language: sourceLanguage,
                    target_language: targetLanguage
                }),
            });

            if (!response.ok) {
                throw new Error('Translation failed');
            }

            const data = await response.json();
            setTranslatedText(data.translated_text);
        } catch (error) {
            setTranslatedText(`Error: ${error.message}`);
        } finally {
            setIsTranslating(false);
        }
    };

    // Clean up recognition on component unmount
    useEffect(() => {
        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.abort();
            }
        };
    }, []);

    return (
        <div className="speech-text-container">
            <h1 className="main-title">Multilingual Speech / Text Conversion</h1>
            <form onSubmit={handleTranslate} className={isListening ? 'listening' : ''}>
                <div className="form-group">
                    <label htmlFor="input_text">Enter text to translate:</label>
                    <textarea
                        id="input_text"
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        placeholder="Type or speak your text here"
                        rows="5"
                    />
                    <button
                        type="button"
                        onClick={handleVoiceInput}
                        className="voice-btn"
                    >
                        {isListening ? (
                            <>
                                <span className="mic-animation">🎤</span> Stop Listening
                            </>
                        ) : (
                            <>🎤 Speak Input</>
                        )}
                    </button>
                    {status && (
                        <div id="status">
                            {isListening && <span className="status-icon status-active"></span>}
                            {status.includes('Error') && <span className="status-icon status-error"></span>}
                            {status}
                        </div>
                    )}
                </div>

                <div className="form-group">
                    <label htmlFor="source_language">Select source language:</label>
                    <select
                        id="source_language"
                        value={sourceLanguage}
                        onChange={(e) => setSourceLanguage(e.target.value)}
                    >
                        {languages.map((language) => (
                            <option key={language} value={language}>
                                {language}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="target_language">Select target language:</label>
                    <select
                        id="target_language"
                        value={targetLanguage}
                        onChange={(e) => setTargetLanguage(e.target.value)}
                    >
                        {languages.map((language) => (
                            <option key={language} value={language}>
                                {language}
                            </option>
                        ))}
                    </select>
                </div>

                <button type="submit" disabled={isTranslating || !inputText.trim()}>
                    {isTranslating ? 'Translating...' : 'Translate'}
                </button>
            </form>

            {translatedText && (
                <div className="output">
                    <h3>Translated Text:</h3>
                    <p className={translatedText.startsWith('Error') ? 'error' : ''}>
                        {translatedText}
                    </p>
                    <button
                        type="button"
                        onClick={handleSpeakOutput}
                        className="speak-btn"
                        disabled={isSpeaking}
                    >
                        {isSpeaking ? '🔊 Playing...' : '🔊 Speak Output'}
                    </button>
                    {speechStatus && (
                        <div id="speech-status">
                            {isSpeaking && <span className="status-icon status-active"></span>}
                            {speechStatus.includes('Error') && <span className="status-icon status-error"></span>}
                            {speechStatus}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default SpeechTextConversion; 