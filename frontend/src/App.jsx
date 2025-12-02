import { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import './App.css'; // We'll use App.css for layout styles

function App() {
  const [activeTab, setActiveTab] = useState('business');

  const tabs = [
    { id: 'business', label: 'Business Store' },
    { id: 'science', label: 'Science Store' },
    { id: 'story', label: 'Story Store' },
    { id: 'all', label: 'All-in-One' },
  ];

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Gemini Multi-Store RAG</h1>
      </header>

      <div className="tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="content-area">
        <div className="chat-section">
          <h2>Chat with {tabs.find(t => t.id === activeTab)?.label}</h2>
          {/* Key forces remount when tab changes to clear chat history visually if desired, 
              or remove key to persist state but you'd need to manage message state better */}
          <ChatWindow key={activeTab} storeName={activeTab} />
        </div>
      </div>
    </div>
  );
}

export default App;
