"""
App: Streamlit frontend for the job application agent.
Handles file upload, job description input, analysis display, resume rewriting with human-in-the-loop approval, and rate-limiting.
"""

import streamlit as st
from agent import run_analysis, run_rewrite
from memory.state import AgentState

MAX_ANALYSES_PER_SESSION = 3

def initialize_session_state():
    """Initialize all session state variables if not already set."""

    if "agent_state" not in st.session_state:
        st.session_state.agent_state = None
    if "analysis_count" not in st.session_state:
        st.session_state.analysis_count = 0
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False

def main():
    st.title("MatchForge")
    st.write("Upload your resume and the paste the job description you wish to apply for.")

    initialize_session_state()

    # Rate limit check
    if st.session_state.analysis_count >= MAX_ANALYSES_PER_SESSION:
        st.warning("You have reached the maximum number of analyses for this session. Please refresh to start a new session.")
        st.stop()

    # Input section
    st.subheader("Input")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")
    job_description = st.text_area("Paste the job description here", height=200)

    # Analyse button
    if st.button("Analyse"):
        if not uploaded_file:
            st.error("Please upload a resume PDF.")
            st.stop()
        if not job_description.strip():
            st.error("Please paste a job description.")
            st.stop()

        with st.spinner("Analysing your resume..."):
            try:
                st.session_state.agent_state = run_analysis(uploaded_file, job_description)
                st.session_state.analysis_count += 1
                st.session_state.analysis_complete = True
            except Exception as e:
                st.session_state.analysis_complete = False
                st.error("The AI service is temporarily unavailable. Please try again later.")

    # Results section
    if st.session_state.analysis_complete and st.session_state.agent_state:
        state = st.session_state.agent_state

        st.subheader("Match Score")
        st.metric(label="Match Score", value=f"{state.match_score}/100")
        st.info(state.match_reasoning)

        st.subheader("Skills Analysis")
        st.success("Present: " + ", ".join(state.present_skills))
        st.error("Missing: " + ", ".join(state.missing_skills))

        st.subheader("Resume Rewriter")
        st.write("Review the analysis above. If you would like a rewritten resume optimized for this role, click below.")
        st.info("Note: The rewriter only rephrases your existing experience. It does not fabricate skills you do not have.")

        if st.button("Approve if you want to rewrite your resume"):
            with st.spinner("Rewriting your resume..."):
                try:
                    st.session_state.agent_state = run_rewrite(st.session_state.agent_state)
                except Exception as e:
                    st.error("The AI service is temporarily unavailable. Please try again in a few minutes.")
                    st.stop()

        if state.rewritten_resume:
            st.text_area("Rewritten Resume", value=state.rewritten_resume, height=400)

if __name__ == "__main__":
    main()