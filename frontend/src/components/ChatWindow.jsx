import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { chatWithStore } from '../api';
import './ChatWindow.css';

const ChatWindow = ({ storeName }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const data = await chatWithStore(storeName, input);
            const botMessage = { role: 'bot', content: data.response };
            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            const errorMessage = { role: 'error', content: "Error getting response." };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-window">
            <div className="messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.role}`}>
                        <strong>{msg.role === 'user' ? 'You' : 'Gemini'}:</strong>
                        <div className="message-content">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                    </div>
                ))}
                {isLoading && <div className="message bot"><em>Thinking...</em></div>}
            </div>
            <div className="input-area">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder={`Ask ${storeName}...`}
                    disabled={isLoading}
                />
                <button onClick={handleSend} disabled={isLoading}>Send</button>
            </div>
        </div>
    );
};

export default ChatWindow;
