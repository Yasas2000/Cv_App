# Resume Dataset

This directory contains **real PDF resumes** used for testing the Resume Search Application.

## Dataset Source

This dataset contains **27 resumes** collected from real candidates:
- **21 resumes** from friends and contacts (Software Engineers, QA Engineers, Associate roles)
- **5 sample resumes** created for initial testing (kept for comparison)
- **1 duplicate** (Pudara Dewdini has both QE and SE versions)

All resumes contain typical candidate information including:
- Work experience and job roles
- Technical skills and technologies
- Education background
- Contact information
- Project experience

## Dataset Statistics

### By Role Type:
- **Software Engineers (SE)**: 10 resumes
- **QA Engineers (QA/QE/AQA/AQAE)**: 11 resumes
- **Full Stack/Data Science/Backend/Frontend**: 5 sample resumes
- **Other**: 1 resume

### Resume Files:

#### Real Resumes from Friends (21):
1. Associate QE- Ayodhya.pdf
2. Binari_Dissanayake_SE.pdf
3. CV_AQE_Hareen.pdf
4. Denuwan Avishka_QA.pdf
5. Denuwan Avishka_SE.pdf
6. Erandhi Madhushika (Velaris-SE).pdf
7. Gayathri_Kaushalya_QA.pdf
8. Ishanka Perera_SE.pdf
9. KupeshanthK QA.pdf
10. Minushika Kapuwaththa.pdf
11. Monali Thennakoon QA.pdf
12. Pasindu Siriwardena_SE.pdf
13. Pramod Jayathilaka_SE.pdf
14. Pudara Dewdini-Resume-SE.pdf
15. Pudara Dewdini_Resume-QE.pdf
16. Risini Methmini_QAE.pdf
17. Sachini Nisansala_AQAE(1).pdf
18. Sakuni Sathsarani_QA.pdf
19. Sanduni Batugedara- Associate Quality Assurance Engineer.pdf
20. Viranga Wadduwage - AQA..pdf
21. Waruni Gunasena - SE.pdf
22. Yasas Ekanayake_ASE.pdf

#### Sample Resumes (5):
23. Sarah_Johnson_Senior_React_Developer.pdf
24. Michael_Chen_Full_Stack_Engineer.pdf
25. Emily_Rodriguez_Data_Scientist.pdf
26. David_Kim_Backend_Developer.pdf
27. Jessica_Williams_Frontend_Engineer.pdf


## Test Queries to Try

With this diverse dataset, you can test various queries:

### Role-Based Searches:
- "Find Software Engineers"
- "Show me QA Engineers with automation experience"
- "Looking for Associate Quality Assurance Engineers"

### Skill-Based Searches:
- "Find developers with Python skills"
- "Who knows automation testing?"
- "Find candidates with React experience"
- "Show me people with Java knowledge"

### Experience Level:
- "Find senior developers"
- "Looking for entry-level QA engineers"
- "Show me experienced software engineers"

### Negative Test (should return "I'm not sure"):
- "Find blockchain developers"
- "Looking for Rust engineers"

## How to Add More Resumes

1. Place PDF resume files in this directory
2. Restart the backend server to re-index all resumes:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
3. The system will automatically parse and index new resumes
4. Check terminal for indexing progress

## Privacy & Ethics Notice

⚠️ **Important**: These resumes are from real people who have given permission for their use in this project.

### Best Practices:
- ✅ Get explicit consent before adding any resume
- ✅ Ensure candidates know how their data will be used
- ✅ Remove or anonymize sensitive information if sharing publicly
- ✅ Don't share this dataset outside the project scope
- ✅ Delete resumes if requested by the candidate

### For Production Use:
- Implement proper data protection measures (encryption, access control)
- Comply with GDPR/CCPA and local privacy regulations
- Use secure storage solutions
- Implement audit logs for resume access
- Provide candidates ability to update/delete their information
- Get proper consent with clear terms

## Note for Production

In a production environment, you would:
- Use a proper resume database or storage service (e.g., AWS S3, Azure Blob Storage)
- Implement privacy and data protection measures
- Get proper consent for storing and processing resumes
- Use real, publicly available resumes or your own candidate database
- Implement access controls and audit logs
- Consider anonymization for certain use cases
- Comply with employment and privacy laws

