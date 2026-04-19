
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Load English tokenizer, tagger, parser, NER and word vectors
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spacy model 'en_core_web_sm'...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Ensure NLTK stopwords are downloaded
try:
    stopwords.words('english')
except LookupError:
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')

stop_words = set(stopwords.words('english'))

def process_text(text: str) -> str:
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return " ".join(filtered_tokens)

def extract_entities(text: str):
    doc = nlp(text)
    entities = {
        "skills": [],
        "tech": [],
        "degrees": []
    }
    # This is a simplified example. More sophisticated NER or rule-based systems would be needed.
    # For demonstration, we'll just look for some common patterns or keywords.
    for ent in doc.ents:
        if ent.label_ == "ORG" or ent.label_ == "PRODUCT": # Often skills/tech are tagged as ORG or PRODUCT
            entities["tech"].append(ent.text)
        elif ent.label_ == "EDU": # Education
            entities["degrees"].append(ent.text)
    
    # Add some rule-based skill extraction (example)
    skill_keywords = ["python", "java", "react", "fastapi", "mongodb", "nlp", "machine learning", "data science"]
    for token in doc:
        if token.text in skill_keywords:
            entities["skills"].append(token.text)
            
    return entities
