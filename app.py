import streamlit as st
from src.job_api import fetch_linkedin_job, fetch_naukri_job
from src.helper import extract_text, ask_qroq


def get_job_url(job):
    for key in ("link", "url", "jobUrl", "job_url", "applyUrl", "apply_url"):
        value = job.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


st.set_page_config(page_title="Job Recommendation System", 
                   page_icon=":briefcase:", layout="wide")
st.title("🤖AI JobRecommendation System")
st.markdown("Uplaod your resume and get job recommendations based on your skills and experience.")

uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from resume..."):
        resume_text = extract_text(uploaded_file)

    with st.spinner("Summerizing resume..."):
        summary = ask_qroq(f"summarize the following resume highliting on skills,education and experience: \n\n{resume_text}", max_tokens=500)
    
    with st.spinner("Finding skill gaps..."):
        skill_gap = ask_qroq(f"Analyze this resume and highlight missing skills, certifications, and experience needed for the better opportunities: \n\n{resume_text}", max_tokens=500)

    with st.spinner("Creating future roadmap..."):
        future_roadmap = ask_qroq(f"Based on this resume suggest a future road map to improve career prospects(skills to learn, certifications need ,industry exposure): \n\n{resume_text}", max_tokens=500)

        st.markdown("---")
        st.header("📑 Resume Summary")
        st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.header("🛠️ Skill Gaps & Missing Areas")
        st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{skill_gap}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.header("🚀 Future Roadmap & Preparation Strategy")
        st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{future_roadmap}</div>", unsafe_allow_html=True)

        st.success("✅ Analysis Completed Successfully!")

        if st.button("Get Job Recommendations"):
            with st.spinner("Fetching jobs"):
                keywords = ask_qroq(
                    f"Give ONLY 5 most relevant job titles from this resume. Comma separated, no extra text. \n\n Summary: \n\n{summary}",
                    max_tokens=100)
                search_keywords = str(keywords).replace("\n", "").strip()

            st.success(f"✅ Keywords Extracted: {search_keywords}")

            with st.spinner("Fetching Jobs from LinkedIn and Naukri..."):
                linkedin_jobs = fetch_linkedin_job(search_keywords)
                naukri_jobs = fetch_naukri_job(search_keywords)

            st.markdown("---")
            st.header("💼 Top LinkedIn Jobs")

            if linkedin_jobs:
                for job in linkedin_jobs:
                    st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                    st.markdown(f"- 📍 {job.get('location')}")
                    job_url = get_job_url(job)
                    if job_url:
                        st.markdown(f"- 🔗 [View Job]({job_url})")
                    else:
                        st.markdown("- 🔗 Link unavailable")
                    st.markdown("---")
            else:
                st.warning("No LinkedIn jobs found.")

            st.markdown("---")
            st.header("💼 Top Naukri Jobs (India)")

            if naukri_jobs:
                for job in naukri_jobs:
                    st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                    st.markdown(f"- 📍 {job.get('location')}")
                    job_url = get_job_url(job)
                    if job_url:
                        st.markdown(f"- 🔗 [View Job]({job_url})")
                    else:
                        st.markdown("- 🔗 Link unavailable")
                    st.markdown("---")
            else:
                st.warning("No Naukri jobs found.")


