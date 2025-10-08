from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from resume_processor import ResumeProcessor

app = FastAPI(title="Resume Search API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize resume processor
resume_processor = ResumeProcessor()

class QueryRequest(BaseModel):
    query: str

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
    resumes_dir = os.path.join(os.path.dirname(__file__), "..", "resumes")
    if os.path.exists(resumes_dir):
        resume_processor.index_resumes(resumes_dir)
        print(f"Indexed {len(resume_processor.resumes)} resumes")
    else:
        print("No resumes directory found. Please add resumes to the /resumes folder.")

@app.get("/")
async def root():
    return {
        "message": "Resume Search API",
        "indexed_resumes": len(resume_processor.resumes),
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
    return {"status": "healthy", "indexed_resumes": len(resume_processor.resumes)}

@app.get("/resume/{filename}")
async def get_resume(filename: str):
    """Serve resume PDF files"""
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
