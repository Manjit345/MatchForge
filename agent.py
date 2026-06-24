"""
Agent: Orchestrates the whole project pipeline by coordinating all the tools in sequence, managing shared state and implement humna-in-the-loop approval before rewriting the resume
"""

from tools.pdf_parser import extract_resume_text
from tools.skills_analyzer import analyze_skills_gap
from tools.score_calculator import calculate_match_score
from tools.resume_rewriter import rewrite_resume
from memory.state import AgentState

def run_analysis(pdf_file, job_description: str) -> AgentState:
    """
    Runs the full analysis pipeline on a resume and a specified job description.
    Populates and returns an AgentState object with required results.

    Args:
        pdf_file: PDF file object of the uploaded resume.
        job_description: Plain text of the target job description.

    Returns:
        AgentState: Fully populated state object with resume text, job description, present and missing skills, match score, and reasonings for the skill analysis and matching score.
    """

    state = AgentState()

    state.resume_text = extract_resume_text(pdf_file)
    state.job_description = job_description
    
    skills_analysis = analyze_skills_gap(state.resume_text, state.job_description)
    state.present_skills = skills_analysis.present_skills
    state.missing_skills = skills_analysis.missing_skills
    state.skills_reasoning = skills_analysis.reasoning

    score_analysis = calculate_match_score(state.resume_text, state.job_description)
    state.match_score = score_analysis.match_score
    state.match_reasoning = score_analysis.reasoning

    return state

def run_rewrite(state: AgentState) -> AgentState:
    """
    Run the resume rewrite step after it is approved by the user.

    Args:
        state: Populated AgentState from run_analysis.

    Returns:
        AgentState: Same state object with rewritten_resume populated.
    """
    
    state.rewritten_resume = rewrite_resume(state.resume_text, state.job_description, state.missing_skills)

    return state

#Code for unit testing the agent
if __name__ == "__main__":
    sample_jd = "Looking for a candidate skilled in Python, PyTorch, Docker, and cloud deployment (AWS/GCP)."
    
    with open("sample_resume.pdf", "rb") as pdf_file:
        state = run_analysis(pdf_file, sample_jd)
    
    print(f"Present skills: {state.present_skills}")
    print(f"Missing skills: {state.missing_skills}")
    print(f"Match score: {state.match_score}")
    print(f"Match reasoning: {state.match_reasoning}")