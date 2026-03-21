import streamlit as st
import pandas as pd
import PyPDF2
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Resume Screening", layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
<style>

.main-title{
font-size:42px;
font-weight:bold;
text-align:center;
padding:15px;
color:white;
border-radius:12px;
background: linear-gradient(90deg,#667eea,#764ba2);
}

.metric-card{
padding:15px;
border-radius:10px;
background:#f0f2f6;
text-align:center;
box-shadow:0px 3px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown('<div class="main-title">🤖 AI Resume Screening Platform</div>', unsafe_allow_html=True)

st.write("Upload candidate resumes and evaluate them against a job description using AI matching.")

st.divider()

# ---------- Job Description ----------
st.subheader("📄 Job Description")

job_description = st.text_area(
"Paste job description here",
height=150
)

# ---------- Upload resumes ----------
st.subheader("📁 Upload Candidate Resumes")

uploaded_files = st.file_uploader(
"Upload PDF resumes",
type=["pdf"],
accept_multiple_files=True
)

# ---------- Skill database ----------
skills_db=[
"python","java","sql","machine learning","data science",
"aws","deep learning","nlp","cloud","excel","power bi",
"docker","react","node.js","tensorflow","pytorch"
]

def extract_text(file):

    reader=PyPDF2.PdfReader(file)
    text=""

    for page in reader.pages:
        if page.extract_text():
            text+=page.extract_text()

    return text


def extract_skills(text):

    text=text.lower()

    found=[]

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return found


results=[]

if uploaded_files and job_description:

    st.subheader("🔍 Screening Candidates")

    for file in uploaded_files:

        resume_text=extract_text(file)

        skills=extract_skills(resume_text)

        documents=[job_description,resume_text]

        tfidf=TfidfVectorizer()

        matrix=tfidf.fit_transform(documents)

        score=cosine_similarity(matrix[0:1],matrix[1:2])[0][0]*100

        results.append({
        "Candidate":file.name,
        "Skills":", ".join(skills),
        "Score":round(score,2)
        })

    df=pd.DataFrame(results)

    df=df.sort_values(by="Score",ascending=False)

    st.divider()

    # ---------- Metrics ----------
    top=df.iloc[0]

    col1,col2,col3=st.columns(3)

    col1.metric("📄 Total Resumes",len(df))
    col2.metric("🏆 Top Score",f"{top['Score']}%")
    col3.metric("⭐ Best Candidate",top["Candidate"])

    st.success(f"🏆 Top Candidate: {top['Candidate']} | Score: {top['Score']}%")

    st.divider()

    # ---------- Candidate cards ----------
    st.subheader("👨‍💼 Candidate Profiles")

    for i,row in df.iterrows():

        st.markdown("---")

        col1,col2=st.columns([1,3])

        with col1:
            st.progress(row["Score"]/100)

        with col2:
            st.subheader(row["Candidate"])
            st.write("**Skills:**",row["Skills"])
            st.write("**Match Score:**",row["Score"],"%")

    st.divider()

    # ---------- Ranking table ----------
    st.subheader("📊 Candidate Ranking Table")

    st.dataframe(df,use_container_width=True)

    st.divider()

    # ---------- Score chart ----------
    st.subheader("📈 Resume Match Scores")

    fig=px.bar(
    df,
    x="Candidate",
    y="Score",
    color="Score",
    text="Score",
    color_continuous_scale="viridis"
    )

    st.plotly_chart(fig,use_container_width=True)

    # ---------- Skill distribution ----------
    st.subheader("🧠 Skills Distribution")

    skill_list=[]

    for s in df["Skills"]:
        skill_list.extend(s.split(","))

    skill_df=pd.DataFrame(skill_list,columns=["Skill"])

    fig2=px.histogram(skill_df,x="Skill",color="Skill")

    st.plotly_chart(fig2,use_container_width=True)

    # ---------- Download shortlist ----------
    csv=df.to_csv(index=False)

    st.download_button(
    "📥 Download Shortlisted Candidates",
    csv,
    "shortlisted_candidates.csv",
    "text/csv"
    )

else:
    st.info("Upload resumes and enter a job description to start screening.")