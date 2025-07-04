from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Allow Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class CoverLetterRequest(BaseModel):
    name: str
    skills: list[str]
    locationPref: list[str]
    jobDescription: str

@app.post("/api/generate-cover-letter")
async def generate_cover_letter(data: CoverLetterRequest):
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
Write a personalized, enthusiastic cover letter starting with 'Dear Hiring Manager' based on:
Name: {data.name}
Skills: {', '.join(data.skills)}
Preferred Location: {', '.join(data.locationPref)}
Job Description: {data.jobDescription}

Make it professional, role-specific, ATS-friendly, and ~250 words max.
"""

    response = model.generate_content(prompt)
    return { "coverLetter": response.text.strip() }
