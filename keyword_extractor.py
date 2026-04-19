
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict
import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spacy model \'en_core_web_sm\'...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def rule_based_matching(text: str, predefined_keywords: List[str]) -> List[str]:
    found_keywords = []
    text_lower = text.lower()
    for keyword in predefined_keywords:
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)
    return found_keywords

def tfidf_extraction(documents: List[str], top_n: int = 10) -> List[str]:
    if not documents:
        return []
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    
    # Assuming we are extracting keywords for the last document in the list (the current resume/JD)
    # To extract for a specific document, pass only that document in the list
    response = []
    if tfidf_matrix.shape[0] > 0:
        last_document_vector = tfidf_matrix[-1]
        sorted_items = last_document_vector.nonzero()[1]
        sorted_items = sorted(sorted_items, key=lambda x: last_document_vector[0, x], reverse=True)
        
        for idx in sorted_items[:top_n]:
            response.append(feature_names[idx])
    return response

def ner_extraction(text: str) -> Dict[str, List[str]]:
    doc = nlp(text)
    entities = {
        "skills": [],
        "tech": [],
        "degrees": []
    }
    
    # Example of how to extract specific entities. This can be greatly expanded.
    # For a real-world scenario, custom NER models or more extensive rule-sets would be used.
    for ent in doc.ents:
        # Common labels for skills/tech might be ORG, PRODUCT, LANGUAGE, etc.
        if ent.label_ in ["ORG", "PRODUCT", "LANGUAGE"]:
            entities["tech"].append(ent.text)
        elif ent.label_ == "EDUCATION": # Spacy might tag degrees as part of EDUCATION
            entities["degrees"].append(ent.text)
        # Add more specific rules for skills if needed

    # Simple rule-based skill identification (can be combined with NER)
    skill_list = ["python", "java", "javascript", "react", "angular", "vue", "fastapi", "django", "flask", 
                  "mongodb", "sql", "aws", "azure", "gcp", "docker", "kubernetes", "nlp", "machine learning", 
                  "deep learning", "data science", "pytorch", "tensorflow", "scikit-learn", "git", "agile"]
    
    text_lower = text.lower()
    for skill in skill_list:
        if skill in text_lower and skill not in entities["skills"]:
            entities["skills"].append(skill)
            
    return entities
