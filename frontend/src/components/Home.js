import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

const Home = () => {
  const navigate = useNavigate();

  const handleCardClick = (path) => {
    navigate(path);
  };

  return (
    <div className="home-container">
      <div className="header-section mb-3 text-center">
        <h1 className="main-title mb-2">Inclusive AI Assistant</h1>
        <p className="subtitle mb-1">Empowering communication and interaction for everyone</p>
      </div>

      <div className="container d-flex justify-content-center">
        <div
          className="card card-hover card-1 featured-card"
          style={{ width: '600px' }}
          onClick={() => handleCardClick('/multilingual')}
        >
          <div className="card-icon">🌐</div>
          <div className="card-body">
            <h5 className="card-title">Multilingual AI Communication Assistant using Groq</h5>
            <p className="card-text">
              Experience seamless communication across languages with our AI-powered assistant.
              Convert between speech and text in English, Telugu, and Hindi.
              Get instant responses to your queries in regional languages.
            </p>
            <div className="card-footer">
              <span className="learn-more">Learn More →</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  );
};

export default Home; 