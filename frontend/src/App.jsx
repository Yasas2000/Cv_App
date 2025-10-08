import { useState, useEffect } from 'react'
import './App.css'

const API_URL = import.meta.env.API_URL || 'http://localhost:8000'

function App() {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [resumeSource, setResumeSource] = useState('local') // 'local' or 'uploaded'
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [indexedCount, setIndexedCount] = useState(0)

  // Fetch initial status
  useEffect(() => {
    fetchStatus()
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/`)
      const data = await response.json()
      setIndexedCount(data.indexed_resumes)
      setResumeSource(data.current_source || 'local')
      
      // Fetch uploaded files if source is uploaded
      if (data.current_source === 'uploaded') {
        const uploadedResponse = await fetch(`${API_URL}/uploaded-resumes`)
        const uploadedData = await uploadedResponse.json()
        setUploadedFiles(uploadedData.files)
      }
    } catch (error) {
      console.error('Failed to fetch status:', error)
    }
  }

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

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files)
    if (files.length === 0) return

    setUploading(true)
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    try {
      const response = await fetch(`${API_URL}/upload-resumes`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`)
      }

      const data = await response.json()
      setUploadedFiles(data.files)
      setResumeSource('uploaded')
      setIndexedCount(data.indexed_count)
      console.log('Upload response data:', data)
      // Add success message
      const successMessage = {
        type: 'bot',
        content: `✅ Successfully uploaded and indexed ${data.files.length} resume(s). You can now search through them!`
      }
      setMessages(prev => [...prev, successMessage])
    } catch (error) {
      console.error('Upload error:', error)
      alert('Failed to upload resumes. Please try again.')
    } finally {
      setUploading(false)
      e.target.value = '' // Reset file input
    }
  }

  const handleSourceChange = async (newSource) => {
    if (newSource === resumeSource) return

    if (newSource === 'uploaded' && uploadedFiles.length === 0) {
      alert('Please upload resumes first before switching to uploaded source.')
      return
    }

    try {
      const response = await fetch(`${API_URL}/set-resume-source`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ source: newSource }),
      })

      if (!response.ok) {
        throw new Error(`Failed to switch source: ${response.status}`)
      }

      const data = await response.json()
      setResumeSource(newSource)
      setIndexedCount(data.indexed_count)
      
      const switchMessage = {
        type: 'bot',
        content: `🔄 Switched to ${newSource} resumes. Now searching through ${data.indexed_count} resume(s).`
      }
      setMessages(prev => [...prev, switchMessage])
    } catch (error) {
      console.error('Source switch error:', error)
      alert('Failed to switch resume source. Please try again.')
    }
  }

  const handleClearUploads = async () => {
    if (!confirm('Are you sure you want to clear all uploaded resumes?')) return

    try {
      const response = await fetch(`${API_URL}/clear-uploads`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error(`Failed to clear uploads: ${response.status}`)
      }

      const data = await response.json()
      setUploadedFiles([])
      setResumeSource('local')
      setIndexedCount(data.indexed_count)
      
      const clearMessage = {
        type: 'bot',
        content: `🗑️ Cleared all uploaded resumes. Switched back to local resumes (${data.indexed_count} resumes).`
      }
      setMessages(prev => [...prev, clearMessage])
    } catch (error) {
      console.error('Clear uploads error:', error)
      alert('Failed to clear uploads. Please try again.')
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
        <div className="status-bar">
          <span className="status-item">📊 {indexedCount} resumes indexed</span>
          <span className="status-item">📂 Source: {resumeSource === 'local' ? 'Local Folder' : 'Uploaded'}</span>
        </div>
      </header>

      {/* Resume Source Selection */}
      <div className="source-selector">
        <div className="source-options">
          <label className={`source-option ${resumeSource === 'local' ? 'active' : ''}`}>
            <input
              type="radio"
              name="resumeSource"
              value="local"
              checked={resumeSource === 'local'}
              onChange={() => handleSourceChange('local')}
            />
            <span className="source-label">
              📁 Use Local Resumes Folder
              <small>Search through {indexedCount} local resumes</small>
            </span>
          </label>
          
          <label className={`source-option ${resumeSource === 'uploaded' ? 'active' : ''}`}>
            <input
              type="radio"
              name="resumeSource"
              value="uploaded"
              checked={resumeSource === 'uploaded'}
              onChange={() => handleSourceChange('uploaded')}
              disabled={uploadedFiles.length === 0}
            />
            <span className="source-label">
              ☁️ Use Uploaded Resumes
              <small>{uploadedFiles.length > 0 ? `${uploadedFiles.length} uploaded` : 'Upload resumes first'}</small>
            </span>
          </label>
        </div>

        {/* Upload Section */}
        <div className="upload-section">
          <label className="upload-btn" htmlFor="file-upload">
            {uploading ? '⏳ Uploading...' : '📤 Upload Resumes'}
          </label>
          <input
            id="file-upload"
            type="file"
            multiple
            accept=".pdf"
            onChange={handleFileUpload}
            disabled={uploading}
            style={{ display: 'none' }}
          />
          
          {uploadedFiles.length > 0 && (
            <button 
              className="clear-btn"
              onClick={handleClearUploads}
              disabled={uploading}
            >
              🗑️ Clear Uploads
            </button>
          )}
        </div>

        {/* Uploaded Files List */}
        {uploadedFiles.length > 0 && (
          <div className="uploaded-files">
            <p className="files-header">Uploaded Files ({uploadedFiles.length}):</p>
            <div className="files-list">
              {uploadedFiles.map((file, idx) => (
                <span key={idx} className="file-tag">{file}</span>
              ))}
            </div>
          </div>
        )}
      </div>

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
              ) : (
                <div className="message-content">
                  <strong>Assistant:</strong>
                  {msg.content && <p>{msg.content}</p>}
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
