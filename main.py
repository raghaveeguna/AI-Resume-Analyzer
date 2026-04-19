
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from ..nlp.resume_parser import parse_resume
from ..nlp.text_processor import process_text
from ..nlp.keyword_extractor import rule_based_matching, tfidf_extraction, ner_extraction
from ..core.database import get_database
from ..models.resume_model import Resume, JobDescription
from pymongo import MongoClient
from bson import ObjectId

from .auth import router as auth_router, get_current_user

app = FastAPI(
    title="AI Resume Analyzer API",
    description="API for parsing resumes, extracting keywords, and ranking candidates using NLP techniques.",
    version="1.0.0",
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/", tags=["Root"])
async def read_root(current_user: User = Depends(get_current_user)): # Protected endpoint example
    return {"message": "Welcome to the AI Resume Analyzer API"}

@app.post("/upload-resume/", tags=["Resume Processing"])
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, and plain text are supported.")

    db = get_database()
    resumes_collection = db["resumes"]

    resume_text = await parse_resume(file)
    processed_text = process_text(resume_text)

    # Predefined keywords for rule-based matching (example)
    predefined_keywords = ["python", "java", "react", "fastapi", "mongodb", "nlp", "machine learning", "data science", "aws", "docker"]
    rule_keywords = [Keyword(type="rule_based", value=kw) for kw in rule_based_matching(processed_text, predefined_keywords)]

    # TF-IDF (requires multiple documents for meaningful results, here we'll just use the current resume as a single document for demonstration)
    tfidf_keywords = [Keyword(type="tfidf", value=kw) for kw in tfidf_extraction([processed_text])]

    # NER extraction
    ner_entities = ner_extraction(resume_text)
    ner_keywords = []
    for entity_type, entities in ner_entities.items():
        for entity in entities:
            ner_keywords.append(Keyword(type=entity_type, value=entity))

    all_keywords = rule_keywords + tfidf_keywords + ner_keywords

    resume_data = Resume(
        filename=file.filename,
        content_type=file.content_type,
        raw_text=resume_text,
        processed_text=processed_text,
        extracted_keywords=all_keywords,
        ner_entities=ner_entities
    )

    result = resumes_collection.insert_one(resume_data.model_dump(by_alias=True))
    resume_data.id = str(result.inserted_id)

    return JSONResponse(content={
        "message": "Resume uploaded, processed, and stored successfully.",
        "resume_id": resume_data.id,
        "filename": resume_data.filename,
        "extracted_keywords": [kw.model_dump() for kw in resume_data.extracted_keywords]
    })

@app.post("/analyze-job-description/", tags=["Job Description Analysis"])
async def analyze_job_description(jd_text: str):
    db = get_database()
    jds_collection = db["job_descriptions"]

    processed_jd_text = process_text(jd_text)

    predefined_keywords = ["python", "java", "react", "fastapi", "mongodb", "nlp", "machine learning", "data science", "aws", "docker"]
    rule_keywords = [Keyword(type="rule_based", value=kw) for kw in rule_based_matching(processed_jd_text, predefined_keywords)]

    tfidf_keywords = [Keyword(type="tfidf", value=kw) for kw in tfidf_extraction([processed_jd_text])]

    ner_entities = ner_extraction(jd_text)
    ner_keywords = []
    for entity_type, entities in ner_entities.items():
        for entity in entities:
            ner_keywords.append(Keyword(type=entity_type, value=entity))

    all_keywords = rule_keywords + tfidf_keywords + ner_keywords

    jd_data = JobDescription(
        title="Job Description", # Assuming title will be provided or extracted later
        raw_text=jd_text,
        processed_text=processed_jd_text,
        extracted_keywords=all_keywords,
        ner_entities=ner_entities
    )

    result = jds_collection.insert_one(jd_data.model_dump(by_alias=True))
    jd_data.id = str(result.inserted_id)

    return JSONResponse(content={
        "message": "Job description analyzed and stored successfully.",
        "jd_id": jd_data.id,
        "extracted_keywords": [kw.model_dump() for kw in jd_data.extracted_keywords]
    })

@app.get("/candidates/rank/", tags=["Candidate Ranking"])
async def rank_candidates():
    db = get_database()
    resumes_collection = db["resumes"]
    jds_collection = db["job_descriptions"]

    # For demonstration, let's assume we want to rank all resumes against the latest JD
    latest_jd = jds_collection.find_one(sort=[("creation_date", -1)])
    if not latest_jd:
        raise HTTPException(status_code=404, detail="No job descriptions found for ranking.")
    
    jd_keywords = {kw["value"].lower() for kw in latest_jd["extracted_keywords"]}

    ranked_candidates = []
    for resume_doc in resumes_collection.find():
        resume = Resume(**resume_doc)
        resume_keywords = {kw.value.lower() for kw in resume.extracted_keywords}
        
        # Simple matching score
        matching_keywords = resume_keywords.intersection(jd_keywords)
        score = len(matching_keywords) / len(jd_keywords) if jd_keywords else 0
        
        resume.candidate_score = score * 100 # Percentage score
        resumes_collection.update_one({"_id": resume_doc["_id"]}, {"$set": {"candidate_score": resume.candidate_score}})
        
        ranked_candidates.append({
            "resume_id": str(resume.id),
            "filename": resume.filename,
            "score": resume.candidate_score
        })
    
    ranked_candidates.sort(key=lambda x: x["score"], reverse=True)

    return JSONResponse(content={
        "message": "Candidates ranked successfully against the latest job description.",
        "job_description_id": str(latest_jd["_id"]),
        "ranked_candidates": ranked_candidates
    })

