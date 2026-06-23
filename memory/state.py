"""
Agent State: The shared state structure that flows through the agent's pipeline.
Each field represents one piece of information produced or consumed by the agent's tools.
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AgentState:
    """
    Shared state object passed between agent tools during one analysis session.
    All the fields are set as None by default until populated by their respective tools.
    """
    resume_text: Optional[str] = None
    job_description: Optional[str] = None
    present_skills: Optional[List[str]] = None
    missing_skills: Optional[List[str]] = None
    skills_reasoning: Optional[str] = None
    match_score: Optional[float] = None
    match_reasoning: Optional[str] = None
    rewritten_resume: Optional[str] = None

#Code for unit testing the dataclass
if __name__ == "__main__":
    state = AgentState(
        resume_text="Experienced in Python and SQL.",
        job_description="Looking for Python, PyTorch, and Docker skills."
    )
    print(state)
    print(f"Resume text set: {state.resume_text is not None}")
    print(f"Skills gap set: {state.missing_skills is not None}")