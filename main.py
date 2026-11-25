from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()
model = joblib.load("model.pkl")  # trained pipeline saved from the notebook


class Job(BaseModel):
    title: str
    company_profile: str = ""
    description: str = ""
    requirements: str = ""

    # Must match training values ('Unknown' with capital U)
    employment_type: str = "Unknown"
    required_experience: str = "Unknown"
    required_education: str = "Unknown"

    telecommuting: int = 0
    has_company_logo: int = 0
    has_questions: int = 0


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/predict")
def predict(job: Job):
    # Rebuild the same combined "text" column used in training
    text = f"{job.title} {job.company_profile} {job.description} {job.requirements}"

    row = pd.DataFrame([{
        "text": text,
        "telecommuting": job.telecommuting,
        "has_company_logo": job.has_company_logo,
        "has_questions": job.has_questions,
        "employment_type": job.employment_type or "Unknown",
        "required_experience": job.required_experience or "Unknown",
        "required_education": job.required_education or "Unknown",
    }])

    pred = int(model.predict(row)[0])
    prob = float(model.predict_proba(row)[0][1])  # probability of fraud 

    return {
        "prediction": "Fake" if pred == 1 else "Real",
        "fraud_probability": round(prob, 2),
    }

# Run with:  uvicorn main:app --reload
