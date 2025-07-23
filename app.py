import streamlit as st
import uuid
import os
import pandas as pd

from resume_parser import get_resume_data
from database import insert_into_db, client
from matcher import match_requirements
from utils import delete_all

# MongoDB Collection
collection = client["Resume_Database"]["Resume_Collection"]

# App Config
st.set_page_config(page_title="AI Resume Matcher", layout="wide")

st.sidebar.title("Admin Panel")
if st.sidebar.button("🗑️ Clear Database"):
    delete_all(collection)
    st.sidebar.success("Resume database cleared!")

st.title("📄 AI Resume Matcher")
st.markdown("Upload resumes and provide job requirements to get **match scores** instantly.")

# Resume Upload
with st.expander("📤 Upload Resumes", expanded=True):
    resumes = st.file_uploader("Upload one or more resumes (PDF)", type="pdf", accept_multiple_files=True)

# Job Description Input
with st.expander("📝 Job Requirements", expanded=True):
    default_skills = "python, java, c++, sql, nosql, machine learning, tensorflow, seaborn"
    jd_input = st.text_input("Enter Required Skills (comma-separated):", value=default_skills)
    req_skills = [skill.strip().lower() for skill in jd_input.split(",") if skill.strip()]

# Resume Processing
if resumes:
    st.info(f"Processing {len(resumes)} resumes...")
    progress = st.progress(0)

    for idx, resume in enumerate(resumes):
        temp_filename = f"./temp_{uuid.uuid4().hex}.pdf"
        with open(temp_filename, "wb") as f:
            f.write(resume.getvalue())

        resume_data = get_resume_data(temp_filename)
        insert_into_db(resume_data)
        os.remove(temp_filename)

        progress.progress((idx + 1) / len(resumes))

    st.success("✅ All resumes processed!")

    # Matching 
    df = match_requirements(req_skills)
    df = df.sort_values("Match_Percent", ascending=False).reset_index(drop=True)

    st.subheader("📊 Match Results")
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "📥 Download CSV",
        data=df.to_csv(index=False),
        file_name="resume_match_results.csv",
        mime="text/csv"
    )
else:
    st.warning("Please upload at least one resume to begin.")
