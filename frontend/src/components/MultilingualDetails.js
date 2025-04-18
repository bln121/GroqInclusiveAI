import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

const MultilingualDetails = () => {
  const navigate = useNavigate();

  const handleCardClick = (path) => {
    navigate(path);
  };

  return (
    <div className="home-container">
      <div className="header-section">
        <h1 className="main-title">Multilingual AI Communication Assistant</h1>
        <p className="subtitle">Bridging Language Barriers Through AI Technology</p>
      </div>

      <div className="cards-container">
        <div className="row">
          <div className="col-md-6 mb-4">
            <div
              className="card card-hover card-1 featured-card"
              onClick={() => handleCardClick('/multilingual/speech-text-conversion')}
            >
              <div className="card-icon">
                <div className="icon-wrapper">
                  <span className="animation-wave">🎤</span>
                </div>
              </div>
              <div className="card-body">
                <h5 className="card-title">Multilingual Speech/Text Conversion</h5>
                <p className="card-text">
                  Convert between speech and text in multiple languages using advanced AI models.
                  Supports diverse users with real-time, multilingual voice and text interaction.
                </p>
                <div className="features-list">
                  <span className="feature-badge">5 Languages</span>
                </div>
                <div className="card-footer">
                  <button className="try-now-btn">Try Now <span className="arrow">→</span></button>
                </div>
              </div>
            </div>
          </div>

          <div className="col-md-6 mb-4">
            <div
              className="card card-hover card-2 featured-card"
              onClick={() => handleCardClick('/multilingual/chatbot')}
            >
              <div className="card-icon">
                <div className="icon-wrapper">
                  <span className="animation-pulse">💬</span>
                </div>
              </div>
              <div className="card-body">
                <h5 className="card-title">AI Chatbot</h5>
                <p className="card-text">
                  A conversational assistant that handles queries in regional languages.
                  Provides quick, context-aware responses, supporting both general and sensory-impaired users.
                </p>
                <div className="features-list">
                  <span className="feature-badge">Conversational AI</span>
                  <span className="feature-badge">Multilingual</span>
                  <span className="feature-badge">Accessibility</span>
                </div>
                <div className="card-footer">
                  <button className="try-now-btn">Try Now <span className="arrow">→</span></button>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default MultilingualDetails; 