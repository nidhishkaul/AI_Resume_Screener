import streamlit as st
from resume_parser import get_resume_data
from database import insert_into_db
from matcher import match_requirements
from database import client
from utils import delete_all
import uuid
import os

collection = client["Resume_Database"]["Resume_Collection"]

req_skills = ["python", "java", "c++", "sql", "nosql", "machine learning", "tensorflow", "seaborn"]

if st.sidebar.button("Empty DataFrame"):
    delete_all(collection)


resumes = st.file_uploader("Upload your resume",type="pdf",accept_multiple_files=True)
if resumes:
    for resume in resumes:
        temp_filename = f"./temp_{uuid.uuid4().hex}.pdf"
        with open(temp_filename, "wb") as f:
            f.write(resume.getvalue())
        resume_data = get_resume_data(temp_filename)
        insert_into_db(resume_data)
        os.remove(temp_filename)
    df = match_requirements(req_skills)
    st.dataframe(df)