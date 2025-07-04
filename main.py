from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

class ChatRequest(BaseModel):
    name: str
    skills: list
    education: str
    experience: str
    jobDescription: str

@app.post("/chat")
def chat(req: ChatRequest):
    prompt = f"""
You are an AI assistant helping {req.name} apply for jobs. Based on this job description:

{req.jobDescription}

Generate a tailored **resume** (based on:
Skills: {', '.join(req.skills)}
Education: {req.education}
Experience: {req.experience}
) and a **cover letter**.

Reply in this format:
---
**Resume**
<resume content>

---
**Cover Letter**
<cover letter content>
"""
    try:
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
