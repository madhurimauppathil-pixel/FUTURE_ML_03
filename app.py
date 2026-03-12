import subprocess, sys

try:
    import spacy
    spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from resume_screener import ResumeScreener
from sample_data import JOB_DATA_SCIENTIST, JOB_BACKEND_ENGINEER, RESUMES

st.set_page_config(page_title="Resume Screener", layout="wide", page_icon="📄")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("⚙️ Configuration")

job_choice = st.sidebar.selectbox(
    "Select Job Role",
    ["Senior Data Scientist", "Backend Software Engineer"]
)
job = JOB_DATA_SCIENTIST if job_choice == "Senior Data Scientist" else JOB_BACKEND_ENGINEER

st.sidebar.markdown("---")
st.sidebar.markdown("### Upload Custom Resume")
uploaded = st.sidebar.file_uploader("Upload .txt resume", type=["txt"], accept_multiple_files=True)

# ── Run Screener ──────────────────────────────────────────────────────────────
screener = ResumeScreener()

resumes = list(RESUMES)
if uploaded:
    for f in uploaded:
        resumes.append({"name": f.name.replace(".txt", ""), "text": f.read().decode()})

with st.spinner("Screening candidates..."):
    df = screener.screen(resumes, job)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📄 Resume Screening Dashboard")
st.subheader(f"Role: {job['title']}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Candidates", len(df))
col2.metric("Top Score", f"{df['total_score'].max():.1f}/100")
col3.metric("Avg Score", f"{df['total_score'].mean():.1f}/100")
strong = len(df[df['total_score'] >= 75])
col4.metric("Strong Matches (≥75)", strong)

st.markdown("---")

# ── Row 1: Overall Score + Breakdown ─────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### 🏆 Overall Candidate Score")
    colors = df['total_score'].apply(
        lambda s: "#2ecc71" if s >= 75 else "#f39c12" if s >= 55 else "#e74c3c"
    )
    fig1 = go.Figure(go.Bar(
        x=df['total_score'], y=df['name'], orientation='h',
        marker_color=list(colors),
        text=[f"{s:.1f} [{g}]" for s, g in zip(df['total_score'], df['grade'])],
        textposition='outside'
    ))
    fig1.add_vline(x=75, line_dash="dash", line_color="#3498db",
                   annotation_text="Strong Match (75)")
    fig1.add_vline(x=55, line_dash="dash", line_color="#f39c12",
                   annotation_text="Moderate (55)")
    fig1.update_layout(xaxis_range=[0, 115], xaxis_title="Score (out of 100)",
                       yaxis=dict(autorange="reversed"), height=350, margin=dict(l=10))
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("#### 📊 Score Breakdown by Component")
    short_names = df['name'].str.split().str[0]
    fig2 = go.Figure()
    fig2.add_bar(name="Semantic (45%)", x=short_names, y=df['tfidf_similarity'],
                 marker_color="#3498db")
    fig2.add_bar(name="Skills (40%)", x=short_names, y=df['skill_match_score'],
                 marker_color="#2ecc71")
    fig2.add_bar(name="Experience (15%)", x=short_names, y=df['experience_score'],
                 marker_color="#e67e22")
    fig2.update_layout(barmode='group', height=350,
                       yaxis_title="Component Score (0–100)")
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Skill Heatmap + Bubble ────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown("#### 🔥 Required Skills Coverage")
    required = job['required_skills']
    heatmap_data = []
    for _, row in df.iterrows():
        matched = set(row['matched_required'])
        heatmap_data.append([1 if s in matched else 0 for s in required])
    hm = pd.DataFrame(heatmap_data, index=df['name'].str.split().str[0], columns=required)
    fig3 = px.imshow(hm, color_continu
