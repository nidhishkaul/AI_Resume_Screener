import streamlit as st
import uuid
import os
import pandas as pd
from resume_parser import get_resume_data
from matcher import match_requirements

# App Config
st.set_page_config(page_title="AI Resume Matcher", layout="wide")
st.markdown("<h1 style='text-align: center;'>📄 AI Resume Matcher</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Upload resumes and get job match scores instantly using AI</h4>", unsafe_allow_html=True)
st.markdown("---")

if "resume_data" not in st.session_state:
    st.session_state["resume_data"] = []

# Resume Upload Section
with st.container():
    with st.expander("📤 Upload Resumes", expanded=True):
        st.markdown("Upload one or more **PDF resumes**:")
        resumes = st.file_uploader("Choose Resumes", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

# Job Requirements Section 
with st.container():
    with st.expander("📝 Enter Job Requirements", expanded=True):
        st.markdown("Provide a **comma-separated list** of required skills for the job:")
        default_skills = "python, java, c++, sql, nosql, machine learning, tensorflow, seaborn"
        jd_input = st.text_input("Required Skills:", value=default_skills)
        req_skills = [skill.strip().lower() for skill in jd_input.split(",") if skill.strip()]

#  Match Button 
col1, col2, _ = st.columns([1, 1, 6])
with col1:
    match_clicked = st.button("🔍 Match Resumes", use_container_width=True)
with col2:
    clear_clicked = st.button("🗑️ Clear Results", use_container_width=True)

# Resume Processing
if match_clicked:
    if not resumes:
        st.warning("⚠️ Please upload at least one resume.")
    elif not req_skills:
        st.warning("⚠️ Please enter required skills.")
    else:
        st.info(f"⏳ Processing {len(resumes)} resumes. Please wait...")
        progress = st.progress(0)

        new_data = []
        for idx, resume in enumerate(resumes):
            temp_filename = f"./temp_{uuid.uuid4().hex}.pdf"
            with open(temp_filename, "wb") as f:
                f.write(resume.read())

            try:
                parsed_data = get_resume_data(temp_filename)
                os.remove(temp_filename)

                cand_skills = [skill.lower() for skill in parsed_data.get("skills", [])]
                score = match_requirements(req_skills, cand_skills)

                parsed_data["match_percent"] = round(float(score), 2)
                new_data.append(parsed_data)

            except Exception as e:
                st.error(f"❌ Error processing {resume.name}: {e}")

            progress.progress((idx + 1) / len(resumes))

        st.session_state["resume_data"].extend(new_data)
        st.success("✅ All resumes processed successfully!")

# Clear Button Logic
if clear_clicked:
    st.session_state["resume_data"] = []
    st.success("🧹 All match results cleared!")

# Display Results
if st.session_state["resume_data"]:
    df = pd.DataFrame(st.session_state["resume_data"])
    df_display = df[["name", "email", "contact_number", "location", "skills", "match_percent"]]

    st.markdown("### 📊 Match Results")

    # Metric display for each candidate
    st.markdown("#### 🔢 Candidate Match Scores")
    for idx, row in df_display.iterrows():
        col = st.columns(2)
        col[0].markdown(f"**👤 {row['name']}**")
        col[1].progress(row["match_percent"] / 100.0, f"{row['match_percent']}%")

    # Show table
    st.markdown("#### 📋 Complete Match Data")
    st.dataframe(df_display, use_container_width=True)

    # Download CSV
    csv = df_display.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "resume_match_results.csv", "text/csv", use_container_width=True)

