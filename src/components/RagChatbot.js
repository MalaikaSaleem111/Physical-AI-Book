import React, { useState, useRef, useEffect } from 'react';
import './RagChatbot.css';

// ===== Main Chatbot Component =====
const RagChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Capture selected text on page
  useEffect(() => {
    const handleSelection = () => {
      setTimeout(() => {
        const selText = window.getSelection().toString().trim();
        if (selText) setSelectedText(selText);
      }, 0);
    };
    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  // Send message to backend
  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { type: 'user', content: inputValue, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const requestBody = {
        q: inputValue,
        selected: selectedText ? String(selectedText) : null
      };

      console.log("Sending request:", JSON.stringify(requestBody)); // debug

      const response = await fetch('http://localhost:8000/rag', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();

      const botMessage = {
        type: 'bot',
        content: data.answer,
        sources: data.sources || [],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [
        ...prev,
        {
          type: 'bot',
          content: 'Sorry, I encountered an error while processing your request. Please try again.',
          timestamp: new Date()
        }
      ]);
    } finally {
      setIsLoading(false);
      setSelectedText('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSelectedText('');
  };

  return (
    <div className="rag-chatbot">
      <div className="chat-header">
        <h3>Physical AI Book Assistant</h3>
        <button onClick={clearChat} className="clear-chat-btn">Clear Chat</button>
      </div>

      {selectedText && (
        <div className="selected-text-preview">
          <strong>Selected text:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
        </div>
      )}

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your Physical AI Book Assistant.</p>
            <p>You can:</p>
            <ul>
              <li>Ask questions about the book content</li>
              <li>Select text on the page and ask questions about it</li>
              <li>Get answers based on the book's content</li>
            </ul>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-content">
                <p>{message.content}</p>
                {message.sources && message.sources.length > 0 && (
                  <div className="sources">
                    <details>
                      <summary>Sources</summary>
                      {message.sources.map((source, idx) => (
                        <div key={idx} className="source-item">
                          <p><strong>From:</strong> {source.source_file}</p>
                          <p><strong>Relevance:</strong> {(source.relevance_score || 0).toFixed(2)}</p>
                          <p>{source.content}</p>
                        </div>
                      ))}
                    </details>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot">
            <div className="message-content">
              <p>Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <textarea
          ref={inputRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about the book content..."
          rows="3"
          disabled={isLoading}
          className="chat-input"
        />
        <button
          onClick={sendMessage}
          disabled={!inputValue.trim() || isLoading}
          className="send-button"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

// ===== Floating Chat Widget Wrapper =====
export const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => setIsOpen(!isOpen);

  return (
    <div>
      {/* Floating Bubble Button */}
      <button className="chat-bubble-btn" onClick={toggleChat}>
        {isOpen ? '✖' : '💬'}
      </button>

      {/* Chatbox */}
      {isOpen && (
        <div className="chatbox-container">
          <RagChatbot />
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
