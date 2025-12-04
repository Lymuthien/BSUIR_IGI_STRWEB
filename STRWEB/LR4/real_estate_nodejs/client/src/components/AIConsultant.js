import React, { useState, useRef, useEffect } from 'react';
import { aiAPI } from '../services/api';
import '../styles/AIConsultant.css';

// Функциональный компонент с хуками для AI консультанта
const AIConsultant = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your real estate consultant. How can I help you today?'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message
    const newUserMessage = { role: 'user', content: userMessage };
    setMessages(prev => [...prev, newUserMessage]);
    setLoading(true);

    try {
      const response = await aiAPI.consultation(userMessage);
      const aiResponse = {
        role: 'assistant',
        content: response.data.response
      };
      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I\'m having trouble connecting. Please try again later.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend(e);
    }
  };

  const handleClear = () => {
    setMessages([
      {
        role: 'assistant',
        content: 'Hello! I\'m your real estate consultant. How can I help you today?'
      }
    ]);
  };

  return (
    <div className="ai-consultant">
      <div className="consultant-header">
        <h4>
          <i className="bi bi-robot"></i> AI Consultant
        </h4>
        <button onClick={handleClear} className="btn btn-sm btn-outline-secondary">
          Clear Chat
        </button>
      </div>
      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={`message message-${message.role}`}>
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message message-assistant">
            <div className="message-content">
              <span className="typing-indicator">Typing...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSend} className="consultant-input-form">
        <input
          type="text"
          value={inputMessage}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about real estate..."
          className="form-control"
          disabled={loading}
        />
        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={loading || !inputMessage.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default AIConsultant;

