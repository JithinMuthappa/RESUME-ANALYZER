import pdfplumber

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

skills_list = [
    "python","java","machine learning",
    "sql","html","css","flask","deep learning"
]

def extract_skills(text):
    found = []
    for skill in skills_list:
        if skill in text:
            found.append(skill)
    return found
