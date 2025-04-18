import React, { useState, useEffect, useRef } from 'react';
import '../styles/Chatbot.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const Chatbot = () => {
    const [textInput, setTextInput] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [currentSessionId, setCurrentSessionId] = useState(null);
    const [chatSessions, setChatSessions] = useState([]);
    const [isRecording, setIsRecording] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);
    const chatBoxRef = useRef(null);
    const audioPlayerRef = useRef(null);
    const baseUrl = '/api/v1';

    // Load chat sessions on component mount
    useEffect(() => {
        loadChatSessions();
    }, []);

    // Scroll to bottom of chat when history changes
    useEffect(() => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    }, [chatHistory]);

    const loadChatSessions = async () => {
        try {
            const response = await fetch(`${baseUrl}/chat-sessions/`);
            const data = await response.json();
            
            const sessionsArray = Object.entries(data.sessions).map(([sid, info]) => ({
                id: sid,
                created: new Date(info.created).toLocaleString(),
                messageCount: info.message_count
            }));
            
            setChatSessions(sessionsArray);
        } catch (error) {
            console.error("Error loading chat sessions:", error);
        }
    };

    const loadChat = async (sessionId) => {
        try {
            setCurrentSessionId(sessionId);
            setChatHistory([]);
            
            const response = await fetch(`${baseUrl}/text-query/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    query: "load history", 
                    session_id: sessionId, 
                    output_as_voice: false 
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.chat_history) {
                setChatHistory(data.chat_history);
            } else {
                console.warn("No chat history found for session:", sessionId);
            }
        } catch (error) {
            console.error("Error loading chat:", error);
        }
    };

    const startNewChat = () => {
        setCurrentSessionId(null);
        setChatHistory([]);
        loadChatSessions();
    };

    const sendTextQuery = async () => {
        const query = textInput.trim();
        if (!query) return;
        
        // Optimistically add user message to UI
        const userMessage = {
            role: "user",
            content: query,
            time: new Date().toLocaleTimeString()
        };
        
        setChatHistory(prev => [...prev, userMessage]);
        setTextInput('');
        setIsLoading(true);
        
        try {
            const response = await fetch(`${baseUrl}/text-query/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    query, 
                    session_id: currentSessionId, 
                    output_as_voice: false 
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.text_response) {
                setChatHistory(data.chat_history);
            }
            
            setCurrentSessionId(data.session_id);
            loadChatSessions();
        } catch (error) {
            console.error("Error:", error);
            
            // Remove optimistic update if there was an error
            setChatHistory(prev => prev.filter(msg => msg !== userMessage));
        } finally {
            setIsLoading(false);
        }
    };

    const startVoiceRecognition = () => {
        try {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert("Speech recognition is not supported in your browser");
                return;
            }
            
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            
            setIsRecording(true);
            
            recognition.onresult = event => {
                const query = event.results[0][0].transcript;
                setTextInput(query);
                setIsRecording(false);
                sendTextQuery();
            };
            
            recognition.onerror = event => {
                console.error("Speech recognition error", event);
                setIsRecording(false);
            };
            
            recognition.onend = () => {
                setIsRecording(false);
            };
            
            recognition.start();
        } catch (error) {
            console.error("Error starting voice recognition:", error);
            setIsRecording(false);
        }
    };

    const editMessage = async (messageIndex, originalContent) => {
        const newContent = prompt("Edit your message:", originalContent);
        if (!newContent || newContent === originalContent) return;
        
        try {
            const response = await fetch(`${baseUrl}/edit-message/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    session_id: currentSessionId,
                    message_index: messageIndex,
                    new_content: newContent
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.status === "success") {
                setChatHistory(data.chat_history);
                
                // If we edited a user message, we need to regenerate the AI response
                if (messageIndex % 2 === 0) { // User messages are at even indices
                    const response = await fetch(`${baseUrl}/text-query/`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            query: newContent,
                            session_id: currentSessionId,
                            output_as_voice: false
                        })
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        setChatHistory(data.chat_history);
                    }
                }
            }
        } catch (error) {
            console.error("Error editing message:", error);
        }
    };

    const playAudio = async (content, messageIndex) => {
        try {
            const response = await fetch(`${baseUrl}/text-query/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query: content,
                    session_id: currentSessionId,
                    output_as_voice: true
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.audio_response) {
                const audioBlob = base64ToBlob(data.audio_response, 'audio/mpeg');
                const audioUrl = URL.createObjectURL(audioBlob);
                
                // Play audio using HTML audio element
                if (audioPlayerRef.current) {
                    audioPlayerRef.current.src = audioUrl;
                    audioPlayerRef.current.style.display = 'block';
                    audioPlayerRef.current.play().catch(err => console.error("Audio play error:", err));
                    
                    // Hide audio player after playback is complete
                    audioPlayerRef.current.onended = () => {
                        audioPlayerRef.current.style.display = 'none';
                    };
                }
            } else {
                console.warn("No audio response from API");
            }
        } catch (error) {
            console.error("Fetch error:", error);
        }
    };

    // Helper function to convert base64 to Blob
    const base64ToBlob = (base64, mimeType) => {
        const byteCharacters = atob(base64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    };

    // Format text with HTML (code blocks, lists, etc)
    const formatTextToHtml = (text) => {
        // Split text into lines
        const lines = text.split('\n');
        let html = '';
        let inList = false;
        let listType = '';
        let inCodeBlock = false;
        let codeBlockContent = [];

        lines.forEach((line, index) => {
            const trimmedLine = line.trim();

            // Detect code block start/end
            if (trimmedLine.startsWith('```')) {
                if (!inCodeBlock) {
                    // Start of code block
                    inCodeBlock = true;
                    codeBlockContent = [];
                } else {
                    // End of code block
                    inCodeBlock = false;
                    // Close any open list
                    if (inList) {
                        html += listType === 'ol' ? '</ol>' : '</ul>';
                        inList = false;
                        listType = '';
                    }
                    // Normalize and add code block
                    const codeText = normalizeCodeBlockIndentation(codeBlockContent);
                    html += `
                        <pre>
                            <button class="copy-btn" onClick="document.execCommand('copy')">Copy</button>
                            <code>${escapeHtml(codeText)}</code>
                        </pre>
                    `;
                }
                return;
            }

            if (inCodeBlock) {
                // Collect lines inside code block
                codeBlockContent.push(line);
                return;
            }

            // Handle numbered list items (e.g., "1. Text")
            if (trimmedLine.match(/^\d+\.\s/)) {
                if (!inList) {
                    html += '<ol>';
                    inList = true;
                    listType = 'ol';
                }
                const listContent = trimmedLine.replace(/^\d+\.\s/, '');
                html += `<li>${escapeHtml(listContent)}</li>`;
            }
            // Handle bullet list items (e.g., "* Text", "- Text")
            else if (trimmedLine.match(/^[*|-]\s/)) {
                if (!inList) {
                    html += '<ul>';
                    inList = true;
                    listType = 'ul';
                }
                const listContent = trimmedLine.replace(/^[*|-]\s/, '');
                html += `<li>${escapeHtml(listContent)}</li>`;
            }
            // Handle paragraphs or empty lines
            else {
                if (inList) {
                    html += listType === 'ol' ? '</ol>' : '</ul>';
                    inList = false;
                    listType = '';
                }
                if (trimmedLine) {
                    html += `<p>${escapeHtml(trimmedLine)}</p>`;
                } else if (index < lines.length - 1) {
                    html += '<p></p>'; // Add empty paragraph for blank lines
                }
            }
        });

        // Close any open list
        if (inList) {
            html += listType === 'ol' ? '</ol>' : '</ul>';
        }

        // Close any open code block
        if (inCodeBlock) {
            const codeText = normalizeCodeBlockIndentation(codeBlockContent);
            html += `
                <pre>
                    <button class="copy-btn">Copy</button>
                    <code>${escapeHtml(codeText)}</code>
                </pre>
            `;
        }

        return html;
    };

    // Function to normalize indentation in code blocks
    const normalizeCodeBlockIndentation = (lines) => {
        if (lines.length === 0) return '';

        // Filter out empty lines and the closing ``` if present
        const nonEmptyLines = lines.filter(line => line.trim() !== '' && !line.trim().startsWith('```'));

        if (nonEmptyLines.length === 0) return '';

        // Find the minimum common indentation
        let minIndent = Infinity;
        nonEmptyLines.forEach(line => {
            const match = line.match(/^\s*/);
            if (match && match[0].length < minIndent && line.trim().length > 0) {
                minIndent = match[0].length;
            }
        });

        // Normalize indentation by removing the minimum common indent
        return nonEmptyLines
            .map(line => (minIndent > 0 && line.length > minIndent ? line.substring(minIndent) : line))
            .join('\n');
    };

    // Function to escape HTML characters to prevent XSS
    const escapeHtml = (text) => {
        const div = document.createElement('div');
        div.innerText = text;
        return div.innerHTML;
    };

    // Handle keyboard input
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendTextQuery();
        }
    };

    const deleteChat = async (sessionId, e) => {
        e.stopPropagation(); // Prevent triggering parent onClick
        
        try {
            const response = await fetch(`${baseUrl}/chat-session/`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // If the deleted session is the current one, clear the chat
            if (sessionId === currentSessionId) {
                setCurrentSessionId(null);
                setChatHistory([]);
            }
            
            // Remove the deleted session from the state
            setChatSessions(prev => prev.filter(session => session.id !== sessionId));
            setShowDeleteConfirm(null);
        } catch (error) {
            console.error("Error deleting chat:", error);
        }
    };
    
    const confirmDelete = (sessionId, e) => {
        e.stopPropagation(); // Prevent triggering parent onClick
        setShowDeleteConfirm(sessionId);
    };
    
    const cancelDelete = (e) => {
        e.stopPropagation(); // Prevent triggering parent onClick
        setShowDeleteConfirm(null);
    };

    return (
        <div className="container chatbot-container">
            <h1 className="main-title">Multilingual AI Chatbot</h1>
            <p className="subtitle">Ask anything in Multilingual - get answers with your preferred language</p>

            <div className="chat-container">
                <div className="sidebar">
                    <div className="sidebar-header">
                        <i className="bi bi-chat-dots me-2"></i>Chat History
                    </div>
                    {chatSessions.length > 0 ? (
                        chatSessions.map(session => (
                            <div 
                                key={session.id} 
                                className={`chat-session ${session.id === currentSessionId ? 'active' : ''}`} 
                                onClick={() => loadChat(session.id)}
                            >
                                <i className="bi bi-chat-left-text me-2"></i>
                                <div className="session-info">
                                    <div className="session-time">{session.created}</div>
                                    <div className="session-count">{session.messageCount} messages</div>
                                </div>
                                {showDeleteConfirm === session.id ? (
                                    <div className="delete-confirm" onClick={e => e.stopPropagation()}>
                                        <span>Delete?</span>
                                        <button className="confirm-yes" onClick={e => deleteChat(session.id, e)}>
                                            <i className="bi bi-check-circle"></i>
                                        </button>
                                        <button className="confirm-no" onClick={cancelDelete}>
                                            <i className="bi bi-x-circle"></i>
                                        </button>
                                    </div>
                                ) : (
                                    <button className="delete-btn" onClick={e => confirmDelete(session.id, e)}>
                                        <i className="bi bi-trash"></i>
                                    </button>
                                )}
                            </div>
                        ))
                    ) : (
                        <div className="no-sessions">
                            <i className="bi bi-info-circle me-2"></i>No previous chats
                        </div>
                    )}
                </div>
                
                <div className="chat-box" ref={chatBoxRef}>
                    {chatHistory.length > 0 ? (
                        chatHistory.map((msg, index) => (
                            <div key={index} className={`message ${msg.role}-message`}>
                                <div className="message-avatar">
                                    <i className={`bi ${msg.role === 'user' ? 'bi-person-circle' : 'bi-robot'}`}></i>
                                </div>
                                <div className="message-content">
                                    <div 
                                        className="content" 
                                        dangerouslySetInnerHTML={{ __html: formatTextToHtml(msg.content) }} 
                                    />
                                    <span className="time">{msg.time}</span>
                                    
                                    {msg.role === "user" && (
                                        <span 
                                            className="edit-btn" 
                                            onClick={() => editMessage(index, msg.content)}
                                            title="Edit message"
                                        >
                                            <i className="bi bi-pencil-square"></i>
                                        </span>
                                    )}
                                    
                                    {msg.role === "assistant" && (
                                        <span 
                                            className="speaker-icon" 
                                            onClick={() => playAudio(msg.content, index)}
                                            title="Listen"
                                        >
                                            <i className="bi bi-volume-up"></i>
                                        </span>
                                    )}
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="empty-chat">
                            <i className="bi bi-chat-square-text fs-1 mb-3"></i>
                            <p>Start a new conversation in any language</p>
                            <p>The AI will respond in the same language you use</p>
                        </div>
                    )}
                    {isLoading && (
                        <div className="loading-spinner">
                            <div className="spinner-border text-primary" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            <div className="input-group">
                <input
                    type="text"
                    placeholder="Ask me anything in Multilingual..."
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    className="chat-input"
                />
                <button className="mic-button" onClick={startVoiceRecognition} title="Voice input">
                    <i className={`bi ${isRecording ? 'bi-mic-mute-fill' : 'bi-mic-fill'}`}></i>
                </button>
                <button className="send-button" onClick={sendTextQuery} title="Send message" disabled={!textInput.trim()}>
                    <i className="bi bi-send-fill"></i>
                </button>
                <button className="new-chat-button" onClick={startNewChat}>
                    <i className="bi bi-plus-circle me-2"></i>New Chat
                </button>
            </div>

            <audio ref={audioPlayerRef} controls className="audio-player" />
        </div>
    );
};

export default Chatbot;
