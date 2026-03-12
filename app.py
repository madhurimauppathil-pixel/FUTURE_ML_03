import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

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

# ── Custom CSS matching your React dashboard ──────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f7f5f0 !important;
    color: #1a1a1a;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1a1a1a !important;
    padding: 2rem 1.5rem;
}
[data-testid="stSidebar"] * {
    color: #f5f0e8 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f5f0e8 !important;
    font-family: 'Cormorant Garamond', serif !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #2a2a2a !important;
    border: 1px solid #3a3a3a !important;
    color: #f5f0e8 !important;
}

/* Main area */
.main .block-container {
    background-color: #f7f5f0 !important;
    padding: 2.5rem 3rem;
    max-width: 1400px;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #faf8f4;
    border: 1px solid #ddd8ce;
    border-radius: 8px;
    padding: 1rem 1.2rem;
}
[data-testid="metric-container"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 9px !important;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #b0a898 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 2.5rem !important;
    color: #1a1a1a !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #ddd8ce !important;
    border-radius: 8px;
}

/* Expander */
[data-testid="stExpander"] {
    background: #faf8f4 !important;
    border: 1px solid #ddd8ce !important;
    border-radius: 8px !important;
    margin-bottom: 8px;
}
[data-testid="stExpander"] summary {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.4rem !important;
    color: #1a1a1a !important;
}

/* Headings */
h1 { font-family: 'Cormorant Garamond', serif !important; font-weight: 300 !important; letter-spacing: -1px; }
h2, h3 { font-family: 'Cormorant Garamond', serif !important; }

/* Divider */
hr { border-color: #ddd8ce !important; }

/* Skill tags */
.skill-tag {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    background: #e8e4dc;
    color: #2a2a2a;
    border: 1px solid #d0ccc4;
    padding: 3px 9px;
    border-radius: 2px;
    margin: 2px;
}
.skill-tag-missing {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    background: #ede9e2;
    color: #8a7a68;
    border: 1px solid #ccc8bc;
    padding: 3px 9px;
    border-radius: 2px;
    margin: 2px;
    text-decoration: line-through;
}
.skill-tag-pref {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    background: #f5f2ec;
    color: #6a6050;
    border: 1px solid #ccc8bc;
    padding: 3px 9px;
    border-radius: 2px;
    margin: 2px;
}
.section-label {
    font-family: 'Inter', sans-serif;
    font-size: 9px;
    color: #b0a898;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 12px;
}
.score-big {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 400;
    color: #1a1a1a;
    letter-spacing: -1px;
    line-height: 1;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown('<div style="font-family:\'Cormorant Garamond\',serif;font-size:22px;font-weight:500;color:#f5f0e8;margin-bottom:4px;">Resume Screener</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:9px;color:#4a4040;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:24px;">Candidate Analysis</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

job_choice = st.sidebar.selectbox("Select Job Role", ["Senior Data Scientist", "Backend Software Engineer"])
job = JOB_DATA_SCIENTIST if job_choice == "Senior Data Scientist" else JOB_BACKEND_ENGINEER

st.sidebar.markdown("---")
st.sidebar.markdown('<div style="font-size:9px;color:#4a4040;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:8px;">Scoring Weights</div>', unsafe_allow_html=True)
for label, pct in [("Semantic Fit", "45%"), ("Skill Match", "40%"), ("Experience", "15%")]:
    st.sidebar.markdown(f'<div style="display:flex;justify-content:space-between;font-size:11px;color:#6a6050;margin-bottom:4px;"><span>{label}</span><span style="color:#8a7a60;">{pct}</span></div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
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
st.markdown('<div class="section-label">Screening Results</div>', unsafe_allow_html=True)
st.markdown('<h1 style="font-size:3.5rem;font-weight:300;line-height:1.05;margin-bottom:2rem;">Candidate<br><em style="font-style:italic;color:#a09070;">Rankings</em></h1>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Candidates", len(df))
col2.metric("Top Score", f"{df['total_score'].max():.1f}/100")
col3.metric("Avg Score", f"{df['total_score'].mean():.1f}/100")
col4.metric("Strong Matches (≥75)", len(df[df['total_score'] >= 75]))

st.markdown("<br>", unsafe_allow_html=True)

# ── Candidate Cards ───────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Candidates</div>', unsafe_allow_html=True)

for _, row in df.iterrows():
    rank = _.item() if hasattr(_, 'item') else _
    grade = row['grade']
    score = row['total_score']
    initials = row['name'][0]

    with st.expander(f"#{rank}  {row['name']}  —  {score:.1f}/100  [{grade}]"):
        c1, c2, c3 = st.columns(3)
        c1.metric("Skill Match", f"{row['skill_match_score']:.0f}%")
        c2.metric("Semantic Fit", f"{row['tfidf_similarity']:.1f}")
        c3.metric("Experience", f"{row['experience_years']} yrs" if row['experience_years'] > 0 else "N/A")

        st.markdown("<br>", unsafe_allow_html=True)
        left, right = st.columns(2)

        with left:
            st.markdown('<div style="font-size:8px;color:#b0a898;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:8px;">✓ Matched Required</div>', unsafe_allow_html=True)
            tags = " ".join([f'<span class="skill-tag">{s}</span>' for s in row['matched_required']])
            st.markdown(tags or "<span style='color:#b0a898;font-size:12px;'>None</span>", unsafe_allow_html=True)

        with right:
            if row['missing_required']:
                st.markdown('<div style="font-size:8px;color:#b0a898;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:8px;">✗ Missing Required</div>', unsafe_allow_html=True)
                tags = " ".join([f'<span class="skill-tag-missing">{s}</span>' for s in row['missing_required']])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-size:12px;color:#4a4a4a;">No gaps ✨</div>', unsafe_allow_html=True)

            if row['matched_preferred']:
                st.markdown('<div style="font-size:8px;color:#b0a898;text-transform:uppercase;letter-spacing:0.14em;margin:12px 0 8px;">★ Preferred Matched</div>', unsafe_allow_html=True)
                tags = " ".join([f'<span class="skill-tag-pref">{s}</span>' for s in row['matched_preferred']])
                st.markdown(tags, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── Score Analysis Charts ─────────────────────────────────────────────────────
st.markdown('<div class="section-label">Score Analysis</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    short = df['name'].str.split().str[0]
    colors = df['total_score'].apply(lambda s: "#2a2a2a" if s >= 65 else "#a09080" if s >= 45 else "#d0c8bc")
    fig1 = go.Figure(go.Bar(
        x=df['total_score'], y=df['name'], orientation='h',
        marker_color=list(colors),
        text=[f"{s:.1f} [{g}]" for s, g in zip(df['total_score'], df['grade'])],
        textposition='outside', textfont=dict(family="Inter", size=11)
    ))
    fig1.add_vline(x=75, line_dash="dash", line_color="#a09070", line_width=1)
    fig1.update_layout(
        title=dict(text="Overall Score (/100)", font=dict(family="Inter", size=9, color="#b0a898")),
        xaxis_range=[0, 115], xaxis_title="", yaxis=dict(autorange="reversed"),
        height=280, margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="#faf8f4", plot_bgcolor="#faf8f4",
        font=dict(family="Inter"), showlegend=False,
        xaxis=dict(gridcolor="#e8e4dc", gridwidth=1),
        yaxis_showgrid=False
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = go.Figure(go.Bar(
        x=df['skill_match_score'], y=df['name'], orientation='h',
        marker_color="#c8bea8",
        text=[f"{s:.0f}%" for s in df['skill_match_score']],
        textposition='outside', textfont=dict(family="Inter", size=11)
    ))
    fig2.update_layout(
        title=dict(text="Skill Match Score (%)", font=dict(family="Inter", size=9, color="#b0a898")),
        xaxis_range=[0, 115], yaxis=dict(autorange="reversed"),
        height=280, margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="#faf8f4", plot_bgcolor="#faf8f4",
        font=dict(family="Inter"), showlegend=False,
        xaxis=dict(gridcolor="#e8e4dc"), yaxis_showgrid=False
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Skill Matrix ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Skill Matrix</div>', unsafe_allow_html=True)

required = job['required_skills']
heatmap_data = []
for _, row in df.iterrows():
    matched = set(row['matched_required'])
    heatmap_data.append([1 if s in matched else 0 for s in required])

hm = pd.DataFrame(heatmap_data, index=df['name'].str.split().str[0], columns=required)
fig3 = px.imshow(hm, color_continuous_scale=["#ede9e2", "#2a2a2a"],
                 zmin=0, zmax=1, text_auto=True, aspect="auto")
fig3.update_traces(texttemplate="%{z}", textfont=dict(family="Inter", size=11))
fig3.update_layout(
    height=260, coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=10, b=10),
    paper_bgcolor="#faf8f4", plot_bgcolor="#faf8f4",
    font=dict(family="Inter", color="#1a1a1a"),
    xaxis=dict(tickfont=dict(size=10)),
    yaxis=dict(tickfont=dict(size=10))
)
st.plotly_chart(fig3, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div style="display:flex;justify-content:space-between;font-family:\'Cormorant Garamond\',serif;font-size:14px;color:#c0b8a8;font-style:italic;">Resume Screener · Senior Data Scientist<span style="font-family:\'Inter\',sans-serif;font-size:9px;letter-spacing:0.1em;font-style:normal;">scikit-learn · TF-IDF · Python</span></div>', unsafe_allow_html=True)
   
               
