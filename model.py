import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("dataset/resume_dataset.csv")

vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(data["resume_text"])
y = data["role"]

model = LogisticRegression()
model.fit(X, y)

def predict_role(text):
    text_vector = vectorizer.transform([text])
    return model.predict(text_vector)[0]

from sklearn.metrics.pairwise import cosine_similarity

def match_score(resume_text, job_desc):
    resume_vec = vectorizer.transform([resume_text])
    job_vec = vectorizer.transform([job_desc])
    score = cosine_similarity(resume_vec, job_vec)[0][0]
    return round(score * 100, 2)

from sklearn.metrics.pairwise import cosine_similarity

def calculate_match(resume_text, job_description):
    resume_vector = vectorizer.transform([resume_text])
    job_vector = vectorizer.transform([job_description])

    score = cosine_similarity(resume_vector, job_vector)[0][0]
    return round(score * 100, 2)
