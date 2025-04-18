import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/App.css';
import Home from './components/Home';
import MultilingualDetails from './components/MultilingualDetails';
const SpeechTextConversion = React.lazy(() => import('./components/SpeechTextConversion'));
const Chatbot = React.lazy(() => import('./components/Chatbot'));

function App() {
  return (
    <Router>
      <div className="App">
        <React.Suspense fallback={<div>Loading...</div>}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/multilingual" element={<MultilingualDetails />} />
            <Route path="/multilingual/speech-text-conversion" element={<SpeechTextConversion />} />
            <Route path="/multilingual/chatbot" element={<Chatbot />} />
          </Routes>
        </React.Suspense>
      </div>
    </Router>
  );
}

export default App;
