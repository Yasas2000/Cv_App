# 🔍 Resume Search Application

A full-stack AI-powered resume search application that helps hiring managers find the perfect candidates using natural language queries. Built with Python FastAPI backend and React frontend, featuring semantic search capabilities using FAISS vector similarity.

![Resume Search Demo](https://img.shields.io/badge/Status-Ready-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18+-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)

## 🎯 Features

- 🤖 **Natural Language Search**: Ask questions like "Find me candidates with React and Node.js experience who have worked in fintech"
- 🎯 **Semantic Matching**: Uses sentence transformers and FAISS for intelligent candidate matching (>50% relevance threshold)
- 📊 **Match Explanations**: Provides clear explanations for why each candidate matches your requirements
- 💼 **Skills Extraction**: Automatically extracts and displays candidate skills from resumes
- 📱 **Modern UI**: Clean, responsive chat interface for seamless interaction
- 🔗 **Resume Access**: Direct links to original resume PDFs (opens in new tab)
- ❓ **"I'm not sure" Fallback**: Returns helpful message when no good matches are found
- 📤 **Resume Upload**: Upload temporary CVs or use local resume folder
- 🔄 **Dual Source Mode**: Switch between local resumes and uploaded resumes on-the-fly

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ and npm installed

### Step 1: Start the Backend

```powershell
cd backend
pip install -r requirements.txt
python generate_sample_resumes.py  # First time only - generates sample PDFs
uvicorn main:app --reload --port 8000
```

**Note**: On first startup, the backend will download the sentence-transformer model (~80MB) from HuggingFace. This takes 1-2 minutes but only happens once.

### Step 2: Start the Frontend (New Terminal)

```powershell
cd frontend
npm install
npm run dev
```

### Step 3: Use the Application

Open **http://localhost:5173** in your browser and start searching!

**Try these example queries:**
- "Find me candidates with React and Node.js experience"
- "Who has worked in fintech?"
- "Show me data scientists with machine learning experience"
- "Find backend developers with Java and Spring Boot"
- "Find developers with Rust experience" (tests "I'm not sure" response)

## 📁 Project Structure

```
Cv_App/
├── backend/                          # Python FastAPI backend
│   ├── main.py                      # FastAPI application and endpoints
│   ├── resume_processor.py          # Resume parsing and vector search logic
│   ├── generate_sample_resumes.py   # Script to generate sample PDFs
│   ├── requirements.txt             # Python dependencies
│   └── .env.example                 # Environment variables template
├── frontend/                        # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx                  # Main chat interface component
│   │   ├── App.css                  # Application styles
│   │   └── index.css                # Global styles
│   ├── package.json                 # Node dependencies
│   └── vite.config.js               # Vite configuration
├── resumes/                         # Sample PDF resumes
│   └── README.md                    # Dataset documentation
└── README.md                        # This file
```

## 🗂️ Dataset Source

### Sample Resumes Included

The application includes **5 synthetic sample resumes** created specifically for this project:

1. **Sarah Johnson** - Senior React Developer (6 years, Fintech/E-commerce)
2. **Michael Chen** - Full Stack Engineer (5 years, Healthcare/SaaS)
3. **Emily Rodriguez** - Data Scientist (4 years, Fintech/Analytics)
4. **David Kim** - Backend Developer (7 years, Enterprise/Cloud)
5. **Jessica Williams** - Frontend Engineer (3 years, Startup/Consumer Apps)

### Resume Dataset Details

- **Source**: Synthetic resumes generated for demonstration purposes
- **Format**: PDF files with realistic candidate information
- **Content**: Work experience, technical skills, education, contact details
- **Generation**: Created using Python's `reportlab` library (see `backend/generate_sample_resumes.py`)

### Using Real Resumes

To use real resumes:
1. Ensure you have proper consent and comply with data protection regulations (GDPR, CCPA, etc.)
2. Place PDF resume files in the `/resumes` directory
3. Restart the backend server to re-index all resumes

**Note**: This is a demo application. In production, implement proper data security, privacy measures, and access controls.

## 🚀 How to Run the App Locally

### Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- **Git** (optional, for cloning)

### Step 1: Clone or Download the Repository

```bash
git clone <your-repo-url>
cd Cv_App
```

### Step 2: Set Up the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Generate sample PDF resumes:
```bash
pip install reportlab  # Additional dependency for PDF generation
python generate_sample_resumes.py
```

5. Start the backend server:
```bash
python main.py
```

The backend API will run on **http://localhost:8000**

You can verify it's running by visiting:
- http://localhost:8000 - API status
- http://localhost:8000/docs - Interactive API documentation

### Step 3: Set Up the Frontend

1. Open a **new terminal** and navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on **http://localhost:5173**

### Step 4: Use the Application

1. Open your browser and go to **http://localhost:5173**
2. **Choose Resume Source**:
   - **Option A - Local Folder** (default): Uses resumes from `/resumes` folder (27 resumes)
   - **Option B - Upload Resumes**: Click "📤 Upload Resumes" to upload your own PDF files temporarily
3. Type a natural language query in the search box, such as:
   - "Find me candidates with React and Node.js experience"
   - "Who has worked in fintech?"
   - "Show me data scientists with machine learning experience"
4. View matching candidates with their skills, experience, and match explanations
5. Click "View Resume" to open the PDF in a new tab

### Resume Upload Feature

**Upload your own resumes temporarily:**
1. Click "📤 Upload Resumes" button
2. Select one or multiple PDF files from your computer
3. The system will automatically index them and switch to "Uploaded" mode
4. Start searching through your uploaded resumes
5. Click "🗑️ Clear Uploads" to remove uploaded files and return to local mode

**Benefits:**
- ✅ Test the system with your own candidate pool
- ✅ No need to modify the local `/resumes` folder
- ✅ Uploaded files are temporary and not persisted
- ✅ Switch between local and uploaded sources anytime

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework for building APIs
- **FAISS**: Facebook AI Similarity Search for vector similarity
- **sentence-transformers**: Pre-trained models for text embeddings (`all-MiniLM-L6-v2`)
- **pdfplumber**: PDF text extraction and parsing
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI

### Frontend
- **React 18**: UI library for building the interface
- **Vite**: Fast build tool and development server
- **CSS3**: Modern styling with flexbox and animations
- **Fetch API**: For HTTP requests to backend

## 🎯 Design Choices and Tradeoffs

### 1. Vector Search with FAISS
**Choice**: Used FAISS with sentence transformers for semantic search  
**Why**: 
- Fast similarity search even with thousands of resumes
- Captures semantic meaning beyond keyword matching
- Open-source and lightweight (no external API dependencies)

**Tradeoff**: 
- In-memory indexing (not persistent)
- Re-indexes on every server restart
- For production, consider persistent vector databases like Pinecone or Weaviate

### 2. PDF Parsing Strategy
**Choice**: Used pdfplumber for text extraction with regex-based information extraction  
**Why**: 
- Works with most standard PDF formats
- No external API dependencies
- Fast and lightweight

**Tradeoff**: 
- May struggle with complex PDF layouts or scanned documents
- Skills extraction uses keyword matching (could be improved with NLP)
- For production, consider OCR (Tesseract) for scanned PDFs or LLM-based extraction

### 3. Embedding Model
**Choice**: `all-MiniLM-L6-v2` sentence transformer model  
**Why**: 
- Good balance between speed and accuracy
- Small model size (~80MB)
- Runs on CPU without GPU

**Tradeoff**: 
- Not as accurate as larger models (e.g., `all-mpnet-base-v2`)
- For production with more resumes, consider using GPU acceleration

### 4. Frontend Architecture
**Choice**: Single-page React application with chat interface  
**Why**: 
- Intuitive conversational UX for hiring managers
- Real-time feedback with loading states
- Mobile-responsive design

**Tradeoff**: 
- No chat history persistence (resets on page refresh)
- For production, add database storage for conversations and user sessions

### 5. API Design
**Choice**: RESTful API with simple POST endpoint for search  
**Why**: 
- Easy to understand and implement
- Stateless and scalable
- Standard HTTP methods

**Tradeoff**: 
- No pagination (returns top 5 results)
- No filtering or advanced query options
- For production, add parameters for filters (years of experience, location, etc.)

### 6. Data Storage
**Choice**: In-memory storage for indexed resumes  
**Why**: 
- Simple and fast for demo purposes
- No database setup required
- Suitable for small datasets (<1000 resumes)

**Tradeoff**: 
- Data lost on server restart
- Not suitable for large-scale production
- For production, use PostgreSQL with pgvector or dedicated vector DB

## 🔮 Future Enhancements

- [ ] Persistent storage with database (PostgreSQL + pgvector)
- [ ] User authentication and multi-tenant support
- [ ] Advanced filtering (years of experience, location, education)
- [x] Resume upload functionality via UI ✅ (Completed)
- [x] Switch between local and uploaded resume sources ✅ (Completed)
- [ ] PDF viewer integrated in the interface
- [ ] Export search results to CSV/Excel
- [ ] Email notifications for saved searches
- [ ] Improved NLP for skills extraction using spaCy or LLMs
- [ ] A/B testing different embedding models
- [ ] Analytics dashboard for hiring managers
- [ ] Integration with ATS (Applicant Tracking Systems)
- [ ] Drag-and-drop file upload with preview
- [ ] Save uploaded resumes permanently (optional)

## 🧪 Testing

### Backend Testing
```bash
cd backend
# Test the API
curl http://localhost:8000/health

# Test search endpoint
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Find React developers"}'
```

### Frontend Testing
- Navigate through the UI
- Test various natural language queries
- Check responsive design on different screen sizes
- Verify error handling when backend is offline

## 🐛 Troubleshooting

### Backend Issues

**Backend won't start**
- Ensure Python 3.8+ is installed: `python --version`
- Check if all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use: `netstat -ano | findstr :8000` (Windows)

**Model download is slow**
- First-time only: Downloads ~80MB sentence-transformer model from HuggingFace
- Takes 1-2 minutes depending on internet speed
- Subsequent starts will be instant (model is cached)

**No resumes indexed**
- Verify PDF files exist in `/resumes` directory
- Run `python backend/generate_sample_resumes.py` to create sample resumes
- Check backend logs for parsing errors
- Restart backend after adding new PDFs

### Frontend Issues

**Frontend won't start**
- Ensure Node.js 16+ is installed: `node --version`
- If Vite version error, run: `npm install vite@5 @vitejs/plugin-react@4 --save-dev`
- Clear cache and reinstall: `rm -rf node_modules package-lock.json; npm install`
- Check if port 5173 is available (Vite will try 5174 automatically if blocked)

**CORS errors**
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/main.py`
- Update frontend API_URL if using different ports

**"Connection Error" in UI**
- Verify backend is fully started: visit http://localhost:8000
- Check browser console for specific error messages
- Ensure firewall is not blocking localhost connections

**Resume PDF won't open**
- Check browser popup blocker settings
- Verify PDF exists in `/resumes` folder
- Check backend logs for file serving errors
- Try accessing PDF directly: http://localhost:8000/resume/[filename].pdf

### Search Issues

**All candidates returned for irrelevant queries**
- This has been fixed with 50% match threshold
- Queries like "Rust developers" should return "I'm not sure" message
- If still seeing issues, restart backend to reload updated code

**No results for valid queries**
- Try simpler keywords: "React", "Python", "Data Scientist"
- Check if resumes contain those skills (see Dataset section)
- Lower-case variations should work automatically

## 🧪 Testing Guide

### API Endpoints

1. **Health Check**
   ```powershell
   curl http://localhost:8000/health
   ```
   Expected: `{"status": "healthy", "indexed_resumes": 5}`

2. **Search Endpoint**
   ```powershell
   curl -X POST http://localhost:8000/search `
     -H "Content-Type: application/json" `
     -d '{"query": "Find React developers"}'
   ```

3. **Get Resume PDF**
   ```
   http://localhost:8000/resume/Sarah_Johnson_Senior_React_Developer.pdf
   ```

4. **Upload Resumes**
   ```powershell
   # Upload multiple PDF files
   curl -X POST http://localhost:8000/upload-resumes `
     -F "files=@resume1.pdf" `
     -F "files=@resume2.pdf"
   ```

5. **Set Resume Source**
   ```powershell
   # Switch to local resumes
   curl -X POST http://localhost:8000/set-resume-source `
     -H "Content-Type: application/json" `
     -d '{"source": "local"}'
   
   # Switch to uploaded resumes
   curl -X POST http://localhost:8000/set-resume-source `
     -H "Content-Type: application/json" `
     -d '{"source": "uploaded"}'
   ```

6. **Get Uploaded Resumes List**
   ```powershell
   curl http://localhost:8000/uploaded-resumes
   ```

7. **Clear Uploaded Resumes**
   ```powershell
   curl -X DELETE http://localhost:8000/clear-uploads
   ```

8. **API Documentation**
   ```
   http://localhost:8000/docs
   ```

### Test Cases

#### Test 1: Good Match (>50% relevance)
```
Query: "Find React developers with fintech experience"
Expected Results:
- Sarah Johnson (>50% match)
- Explanation includes React and fintech mentions
```

#### Test 2: No Good Match (<50% relevance)
```
Query: "Find developers with Rust and Go experience"
Expected Result:
- "🤔 I'm not sure - I couldn't find any candidates..."
- Helpful suggestions for available skills
```

#### Test 3: Multiple Matches
```
Query: "Full stack engineers"
Expected Results:
- Sarah Johnson, Michael Chen (both >50% match)
- Sorted by relevance score
```

#### Test 4: PDF Opening
```
Steps:
1. Search for "React developer"
2. Click "📄 View Resume" button
3. Verify: PDF opens in NEW browser tab
4. URL: http://localhost:8000/resume/[filename].pdf
```

#### Test 5: Resume Upload Feature
```
Steps:
1. Click "📤 Upload Resumes" button in the UI
2. Select multiple PDF resume files
3. Verify: Files are uploaded and indexed
4. Verify: UI switches to "Uploaded" mode
5. Search query works with uploaded resumes
6. Click "🗑️ Clear Uploads" to remove and return to local
```

#### Test 6: Source Switching
```
Steps:
1. Start with local resumes (default)
2. Upload some PDFs
3. Switch between "Local" and "Uploaded" radio buttons
4. Verify: Search results change based on selected source
5. Verify: Status bar shows correct indexed count
```

#### Test 7: Chat Interface
```
Steps:
1. Type multiple queries in sequence
2. Verify: Chat history displays correctly
3. Verify: Loading states appear during search
4. Verify: Error handling for offline backend
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env` (copy from `.env.example`):
```env
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Configuration

Edit `frontend/src/App.jsx` if backend runs on different port:
```javascript
const API_URL = 'http://localhost:8000'  // Change if needed
```

### Match Threshold

To adjust search sensitivity, edit `backend/resume_processor.py`:
```python
# Line ~159
results = [r for r in results if r['score'] > 0.5]  # Change 0.5 to adjust threshold
```

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed: `python --version`
- Check if all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use: `netstat -ano | findstr :8000` (Windows)

### Frontend won't start
- Ensure Node.js 16+ is installed: `node --version`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 5173 is available

### No resumes indexed
- Verify PDF files exist in `/resumes` directory
- Run `python backend/generate_sample_resumes.py` to create sample resumes
- Check backend logs for parsing errors

### CORS errors
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/main.py`
- Update frontend API_URL if using different ports

## 📝 License

This project is created for educational and demonstration purposes. Feel free to use and modify as needed.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue in the repository.

---

**Note**: This is a demonstration project. For production use, implement proper security measures, data protection compliance, and scalability considerations.
