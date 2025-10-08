import os
import re
import pdfplumber
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import json

class ResumeProcessor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.resumes: List[Dict] = []
        self.index: Optional[faiss.IndexFlatL2] = None
        self.embeddings: Optional[np.ndarray] = None
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def extract_candidate_info(self, text: str, filename: str) -> Dict:
        """Extract structured information from resume text"""
        # Extract name (usually at the top of resume)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        candidate_name = lines[0] if lines else filename.replace('.pdf', '').replace('_', ' ')
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        email = emails[0] if emails else None
        
        # Extract phone
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        phone = phones[0] if phones else None
        
        # Extract skills (common tech keywords)
        text_lower = text.lower()
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'nodejs', 'angular', 
            'vue', 'typescript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'jenkins', 'git', 'agile', 'scrum',
            'machine learning', 'deep learning', 'ai', 'data science', 'tensorflow',
            'pytorch', 'rest api', 'graphql', 'microservices', 'devops',
            'fintech', 'blockchain', 'cybersecurity', 'cloud computing'
        ]
        
        found_skills = [skill for skill in skill_keywords if skill in text_lower]
        
        # Extract experience summary (look for years of experience)
        experience_pattern = r'(\d+)\+?\s*years?\s*(of)?\s*experience'
        experience_match = re.search(experience_pattern, text_lower)
        years_experience = experience_match.group(1) if experience_match else "Not specified"
        
        # Look for job titles and companies
        job_titles = []
        title_keywords = ['engineer', 'developer', 'architect', 'manager', 'analyst', 
                         'consultant', 'specialist', 'lead', 'senior', 'junior']
        for line in lines[:20]:  # Check first 20 lines
            line_lower = line.lower()
            if any(title in line_lower for title in title_keywords):
                job_titles.append(line)
        
        experience_summary = f"{years_experience} years of experience"
        if job_titles:
            experience_summary += f" | Recent role: {job_titles[0]}"
        
        return {
            'name': candidate_name,
            'email': email,
            'phone': phone,
            'skills': found_skills,
            'experience_summary': experience_summary,
            'full_text': text
        }
    
    def index_resumes(self, resumes_dir: str):
        """Index all PDF resumes in the directory"""
        self.resumes = []
        texts_to_embed = []
        
        if not os.path.exists(resumes_dir):
            print(f"Directory {resumes_dir} does not exist")
            return
        
        pdf_files = [f for f in os.listdir(resumes_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in {resumes_dir}")
            return
        
        for filename in pdf_files:
            filepath = os.path.join(resumes_dir, filename)
            text = self.extract_text_from_pdf(filepath)
            
            if not text:
                continue
            
            info = self.extract_candidate_info(text, filename)
            
            resume_data = {
                'id': filename.replace('.pdf', ''),
                'path': filepath,
                'filename': filename,
                **info
            }
            
            self.resumes.append(resume_data)
            texts_to_embed.append(text)
        
        if not texts_to_embed:
            print("No resumes were successfully processed")
            return
        
        # Create embeddings
        print(f"Creating embeddings for {len(texts_to_embed)} resumes...")
        self.embeddings = self.model.encode(texts_to_embed, show_progress_bar=True)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype('float32'))
        
        print(f"Successfully indexed {len(self.resumes)} resumes")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for candidates matching the query"""
        if not self.resumes or self.index is None:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Search in FAISS index
        k = min(top_k, len(self.resumes))
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for idx, (distance, resume_idx) in enumerate(zip(distances[0], indices[0])):
            resume = self.resumes[resume_idx]
            
            # Convert distance to similarity score (lower distance = higher similarity)
            # Normalize to 0-1 range
            score = float(1 / (1 + distance))
            
            # Generate explanation
            explanation = self._generate_explanation(query, resume)
            
            result = {
                'id': resume['id'],
                'name': resume['name'],
                'path': resume['path'],
                'filename': resume['filename'],
                'score': round(score, 3),
                'skills': resume['skills'],
                'experience_summary': resume['experience_summary'],
                'explanation': explanation
            }
            results.append(result)
        
        # Filter out poor matches with more strict threshold
        # Only return candidates with score > 0.5 (50% match)
        results = [r for r in results if r['score'] > 0.5]
        
        return results
    
    def _generate_explanation(self, query: str, resume: Dict) -> str:
        """Generate explanation for why this candidate matches"""
        query_lower = query.lower()
        skills = resume['skills']
        
        # Find matching skills from query
        matching_skills = [skill for skill in skills if skill in query_lower]
        
        explanation_parts = []
        
        if matching_skills:
            explanation_parts.append(f"Has relevant skills: {', '.join(matching_skills[:5])}")
        
        if resume['experience_summary']:
            explanation_parts.append(resume['experience_summary'])
        
        # Check for specific domain mentions in query
        domains = ['fintech', 'healthcare', 'ecommerce', 'e-commerce', 'startup', 'enterprise']
        for domain in domains:
            if domain in query_lower and domain in resume['full_text'].lower():
                explanation_parts.append(f"Experience in {domain}")
        
        if not explanation_parts:
            explanation_parts.append("General experience and skills match the requirements")
        
        return " | ".join(explanation_parts)
