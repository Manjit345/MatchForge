"""
Skills Analyzer: Compares skills mentioned in a resume with those listed as requirements for a job description.
It identifies which of the required skills are present in the resume and which of them are missing.
"""

import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from typing import List
from prompts.templates import SKILLS_GAP_PROMPT

load_dotenv()

class SkillsGapAnalysis(BaseModel):
    present_skills: List[str]
    missing_skills: List[str]
    reasoning: str

def analyze_skills_gap(resume_text:str, job_description:str) -> SkillsGapAnalysis:
    """
    Compare resume against job description to find skill gaps.

    Args:
        resume_text: The text extracted from the candidate's resume.
        job_description: The text of the job description mentioning the required skills.

    Returns:
        SkillsGapAnalysis: A structured object containing lists of present and missing skills, along with reasoning.
    """
    prompt = SKILLS_GAP_PROMPT.format(resume_text=resume_text, job_description=job_description)

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": SkillsGapAnalysis,
        }
    )
    
    return SkillsGapAnalysis.model_validate_json(response.text)

#Code for unit testing the function
if __name__ == "__main__":
    sample_resume = "Experienced in Python, SQL, Git, and basic machine learning with scikit-learn."
    sample_jd = "Looking for a candidate skilled in Python, PyTorch, Docker, and cloud deployment (AWS/GCP)."
    
    result = analyze_skills_gap(sample_resume, sample_jd)
    print(result.model_dump_json(indent=2))