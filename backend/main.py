from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from pathlib import Path
from resume_processor import ResumeProcessor
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Resume Search API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize resume processor
resume_processor = ResumeProcessor()

# Create temp uploads directory
TEMP_UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "temp_uploads")
os.makedirs(TEMP_UPLOADS_DIR, exist_ok=True)

# Track current resume source
current_source = "local"  # "local" or "uploaded"

class QueryRequest(BaseModel):
    query: str

class ResumeSourceRequest(BaseModel):
    source: str  # "local" or "uploaded"

class CandidateResponse(BaseModel):
    candidate_id: str
    candidate_name: str
    resume_path: str
    score: float
    explanation: str
    skills: List[str]
    experience_summary: str

class SearchResponse(BaseModel):
    candidates: List[CandidateResponse]
    message: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Index all resumes on startup"""
    global current_source
    current_source = "local"
    resumes_dir = os.path.join(os.path.dirname(__file__), "..", "resumes")
    if os.path.exists(resumes_dir):
        resume_processor.index_resumes(resumes_dir)
        print(f"Indexed {len(resume_processor.resumes)} resumes from local folder")
    else:
        print("No resumes directory found. Please add resumes to the /resumes folder.")

@app.get("/")
async def root():
    return {
        "message": "Resume Search API",
        "indexed_resumes": len(resume_processor.resumes),
        "current_source": current_source,
        "status": "ready"
    }

@app.post("/search", response_model=SearchResponse)
async def search_candidates(query: QueryRequest):
    """Search for candidates based on natural language query"""
    if not resume_processor.resumes:
        raise HTTPException(
            status_code=503,
            detail="No resumes indexed. Please add resume PDFs to the /resumes folder and restart the server."
        )
    
    if not query.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    results = resume_processor.search(query.query, top_k=5)
    
    if not results:
        return SearchResponse(
            candidates=[],
            message="I'm not sure - I couldn't find any candidates that are a good match for your requirements. Try adjusting your query or using different keywords. Our database includes skills like React, Python, Java, Node.js, Machine Learning, and more."
        )
    
    candidates = []
    for result in results:
        candidate = CandidateResponse(
            candidate_id=result['id'],
            candidate_name=result['name'],
            resume_path=result['path'],
            score=result['score'],
            explanation=result['explanation'],
            skills=result['skills'],
            experience_summary=result['experience_summary']
        )
        candidates.append(candidate)
    
    return SearchResponse(candidates=candidates)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "indexed_resumes": len(resume_processor.resumes),
        "current_source": current_source
    }

@app.post("/upload-resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """Upload multiple resume PDFs temporarily"""
    global current_source
    
    # Clear existing temp uploads
    if os.path.exists(TEMP_UPLOADS_DIR):
        shutil.rmtree(TEMP_UPLOADS_DIR)
    os.makedirs(TEMP_UPLOADS_DIR, exist_ok=True)
    
    uploaded_files = []
    for file in files:
        if not file.filename.endswith('.pdf'):
            continue
        
        file_path = os.path.join(TEMP_UPLOADS_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        uploaded_files.append(file.filename)
    
    # Re-index with uploaded resumes
    if uploaded_files:
        resume_processor.index_resumes(TEMP_UPLOADS_DIR)
        current_source = "uploaded"
        return {
            "message": f"Successfully uploaded and indexed {len(uploaded_files)} resumes",
            "files": uploaded_files,
            "indexed_count": len(resume_processor.resumes)
        }
    else:
        raise HTTPException(status_code=400, detail="No valid PDF files uploaded")

@app.post("/set-resume-source")
async def set_resume_source(request: ResumeSourceRequest):
    """Switch between local and uploaded resume sources"""
    global current_source
    
    if request.source not in ["local", "uploaded"]:
        raise HTTPException(status_code=400, detail="Invalid source. Must be 'local' or 'uploaded'")
    
    if request.source == "local":
        resumes_dir = os.path.join(os.path.dirname(__file__), "..", "resumes")
        if not os.path.exists(resumes_dir):
            raise HTTPException(status_code=404, detail="Local resumes folder not found")
        resume_processor.index_resumes(resumes_dir)
        current_source = "local"
        return {
            "message": f"Switched to local resumes",
            "indexed_count": len(resume_processor.resumes),
            "current_source": current_source
        }
    else:  # uploaded
        if not os.path.exists(TEMP_UPLOADS_DIR) or not os.listdir(TEMP_UPLOADS_DIR):
            raise HTTPException(status_code=404, detail="No uploaded resumes found. Please upload resumes first.")
        resume_processor.index_resumes(TEMP_UPLOADS_DIR)
        current_source = "uploaded"
        return {
            "message": f"Switched to uploaded resumes",
            "indexed_count": len(resume_processor.resumes),
            "current_source": current_source
        }

@app.get("/uploaded-resumes")
async def get_uploaded_resumes():
    """Get list of currently uploaded resumes"""
    if not os.path.exists(TEMP_UPLOADS_DIR):
        return {"files": [], "count": 0}
    
    files = [f for f in os.listdir(TEMP_UPLOADS_DIR) if f.endswith('.pdf')]
    return {"files": files, "count": len(files)}

@app.delete("/clear-uploads")
async def clear_uploads():
    """Clear all uploaded resumes and switch back to local"""
    global current_source
    
    if os.path.exists(TEMP_UPLOADS_DIR):
        shutil.rmtree(TEMP_UPLOADS_DIR)
        os.makedirs(TEMP_UPLOADS_DIR, exist_ok=True)
    
    # Switch back to local resumes
    resumes_dir = os.path.join(os.path.dirname(__file__), "..", "resumes")
    if os.path.exists(resumes_dir):
        resume_processor.index_resumes(resumes_dir)
        current_source = "local"
    
    return {
        "message": "Cleared all uploaded resumes and switched to local",
        "current_source": current_source,
        "indexed_count": len(resume_processor.resumes)
    }

@app.get("/resume/{filename}")
async def get_resume(filename: str):
    """Serve resume PDF files from current source"""
    # Check current source directory first
    if current_source == "uploaded":
        file_path = os.path.join(TEMP_UPLOADS_DIR, filename)
    else:
        resumes_dir = os.path.join(os.path.dirname(__file__), "..", "resumes")
        file_path = os.path.join(resumes_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if not filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
