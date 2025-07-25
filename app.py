import streamlit as st
import uuid
import os
import pandas as pd
from resume_parser import get_resume_data
from matcher import match_requirements

# App Config
st.set_page_config(page_title="AI Resume Matcher", layout="wide")
st.title("📄 AI Resume Matcher")
st.markdown("Upload resumes and provide job requirements to get **match scores** instantly.")

# Session State Initialization
if "resume_data" not in st.session_state:
    st.session_state["resume_data"] = []

# Resume Upload Section
with st.expander("📤 Upload Resumes", expanded=True):
    resumes = st.file_uploader("Upload one or more resumes (PDF)", type="pdf", accept_multiple_files=True)

# Job Description Section
with st.expander("📝 Job Requirements", expanded=True):
    default_skills = "python, java, c++, sql, nosql, machine learning, tensorflow, seaborn"
    jd_input = st.text_input("Enter Required Skills (comma-separated):", value=default_skills)
    req_skills = [skill.strip().lower() for skill in jd_input.split(",") if skill.strip()]

# Resume Processing
if st.button("🔍 Match Resumes"):
    if not resumes:
        st.warning("⚠️ Please upload at least one resume.")
    elif not req_skills:
        st.warning("⚠️ Please enter required skills.")
    else:
        st.info(f"Processing {len(resumes)} resumes...")
        progress = st.progress(0)

        new_data = []
        for idx, resume in enumerate(resumes):
            temp_filename = f"./temp_{uuid.uuid4().hex}.pdf"
            with open(temp_filename, "wb") as f:
                f.write(resume.read())

            try:
                parsed_data = get_resume_data(temp_filename)
                os.remove(temp_filename) # To remove the file once processed

                # Get match score
                cand_skills = [skill.lower() for skill in parsed_data.get("skills", [])]
                score = match_requirements(req_skills, cand_skills)

                parsed_data["match_percent"] = round(float(score), 2)

                new_data.append(parsed_data)
            except Exception as e:
                st.error(f"❌ Error processing {resume.name}: {e}")

            progress.progress((idx + 1) / len(resumes))

        # Update session state
        st.session_state["resume_data"].extend(new_data)
        st.success("✅ All resumes processed!")

# Display Results
if st.session_state["resume_data"]:
    df = pd.DataFrame(st.session_state["resume_data"])
    df_display = df[["name", "email", "contact_number", "location", "skills", "match_percent"]]

    st.subheader("📊 Match Results")
    st.dataframe(df_display, use_container_width=True)

    csv = df_display.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "resume_match_results.csv", "text/csv")

# Clear Session Button
if st.button("🗑️ Clear All Results"):
    st.session_state["resume_data"] = []
    st.success("Session Data Cleared. Rerun the app to start again.")
