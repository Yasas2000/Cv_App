import { useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    
    if (!query.trim()) return

    const userMessage = { type: 'user', content: query }
    setMessages(prev => [...prev, userMessage])
    setLoading(true)
    setQuery('')

    try {
      const response = await fetch(`${API_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      const botMessage = {
        type: 'bot',
        candidates: data.candidates,
        message: data.message,
        query: query
      }
      
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Search error:', error)
      const errorMessage = {
        type: 'bot',
        error: true,
        content: "Sorry, I couldn't connect to the backend. Please make sure the API server is running on port 8000."
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const openResume = (path, candidateName) => {
    // Extract filename from path
    const filename = path.split('\\').pop().split('/').pop();
    
    // Use backend API to serve the PDF
    const resumeUrl = `${API_URL}/resume/${filename}`;
    
    // Open in new tab
    window.open(resumeUrl, '_blank', 'noopener,noreferrer');
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔍 Resume Search Assistant</h1>
        <p>Find the perfect candidates using natural language</p>
      </header>

      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>Welcome! 👋</h2>
              <p>I can help you find candidates from our resume database.</p>
              <div className="example-queries">
                <p><strong>Try asking:</strong></p>
                <ul>
                  <li>"Find me candidates with React and Node.js experience"</li>
                  <li>"Who has worked in fintech?"</li>
                  <li>"Show me senior developers with Python skills"</li>
                  <li>"Find candidates with machine learning experience"</li>
                </ul>
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.type}`}>
              {msg.type === 'user' ? (
                <div className="message-content">
                  <strong>You:</strong> {msg.content}
                </div>
              ) : msg.error ? (
                <div className="message-content error">
                  <strong>Assistant:</strong> {msg.content}
                </div>
              ) : (
                <div className="message-content">
                  <strong>Assistant:</strong>
                  {msg.message && (
                    <p className="no-results">
                      <span className="emoji">🤔</span> {msg.message}
                    </p>
                  )}
                  {msg.candidates && msg.candidates.length > 0 && (
                    <div className="candidates">
                      <p className="results-header">
                        Found {msg.candidates.length} candidate{msg.candidates.length > 1 ? 's' : ''} matching "{msg.query}":
                      </p>
                      {msg.candidates.map((candidate, cidx) => (
                        <div key={cidx} className="candidate-card">
                          <div className="candidate-header">
                            <h3>{candidate.candidate_name}</h3>
                            <span className="match-score">
                              {Math.round(candidate.score * 100)}% match
                            </span>
                          </div>
                          <p className="explanation">{candidate.explanation}</p>
                          {candidate.skills.length > 0 && (
                            <div className="skills">
                              {candidate.skills.slice(0, 8).map((skill, sidx) => (
                                <span key={sidx} className="skill-tag">{skill}</span>
                              ))}
                            </div>
                          )}
                          <button 
                            className="view-resume-btn"
                            onClick={() => openResume(candidate.resume_path, candidate.candidate_name)}
                          >
                            📄 View Resume
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message bot">
              <div className="message-content">
                <strong>Assistant:</strong>
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSearch} className="input-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Describe the candidate you're looking for..."
            disabled={loading}
            className="query-input"
          />
          <button type="submit" disabled={loading || !query.trim()} className="send-btn">
            {loading ? '⏳' : '🚀'} Search
          </button>
        </form>
      </div>
    </div>
  )
}

export default App
