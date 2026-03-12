import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

import streamlit as st
import streamlit.components.v1 as components
import sys, os, json

sys.path.insert(0, os.path.dirname(__file__))
from resume_screener import ResumeScreener
from sample_data import JOB_DATA_SCIENTIST, JOB_BACKEND_ENGINEER, RESUMES

st.set_page_config(page_title="Resume Screener", layout="wide", page_icon="📄")

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

screener = ResumeScreener()
with st.spinner("Loading..."):
    df = screener.screen(RESUMES, JOB_DATA_SCIENTIST)

data = []
for rank, row in df.iterrows():
    data.append({
        "rank": int(rank),
        "name": row["name"],
        "score": round(float(row["total_score"]), 2),
        "tfidf": round(float(row["tfidf_similarity"]), 2),
        "skillScore": int(row["skill_match_score"]),
        "exp": float(row["experience_years"]),
        "gaps": row["missing_required"],
        "matched_skills": row["matched_required"],
        "pref": row["matched_preferred"],
        "grade": row["grade"],
        "fit_label": row["fit_label"],
    })

data_json = json.dumps(data)
req_json = json.dumps(JOB_DATA_SCIENTIST["required_skills"])

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#f7f5f0; }}
::-webkit-scrollbar {{ width:4px; }}
::-webkit-scrollbar-thumb {{ background:#3a3a3a; border-radius:4px; }}
.tog {{ cursor:pointer; transition:background 0.15s; }}
.tog:hover {{ background:#f0ede6 !important; }}
.hrow:hover {{ background:#f0ede6 !important; }}
</style>
</head>
<body>
<div id="root"></div>
<script>
const DATA = {data_json};
const REQ = {req_json};

const {{ useState }} = React;
const gradeLabel = s => s >= 65 ? "Strong" : s >= 45 ? "Moderate" : "Weak";
const ini = n => n[0];

function App() {{
  const [open, setOpen] = useState(null);

  return React.createElement('div', {{
    style: {{ display:"flex", minHeight:"100vh", fontFamily:"Georgia,serif", color:"#1a1a1a", background:"#f7f5f0" }}
  }},

    // ── Sidebar ──
    React.createElement('div', {{
      style: {{ width:300, background:"#1a1a1a", position:"fixed", top:0, left:0, height:"100vh", overflowY:"auto", display:"flex", flexDirection:"column", padding:"48px 36px", flexShrink:0 }}
    }},
      // Title
      React.createElement('div', {{ style:{{ marginBottom:36 }} }},
        React.createElement('div', {{ style:{{ fontFamily:"'Cormorant Garamond',serif", fontSize:22, fontWeight:500, color:"#f5f0e8", letterSpacing:"0.02em", marginBottom:4 }} }}, "Resume Screener"),
        React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", letterSpacing:"0.2em", textTransform:"uppercase" }} }}, "Candidate Analysis")
      ),

      React.createElement('div', {{ style:{{ height:1, background:"#2a2a2a", marginBottom:28 }} }}),

      // Role
      React.createElement('div', {{ style:{{ marginBottom:28 }} }},
        React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.18em", marginBottom:10 }} }}, "Role"),
        React.createElement('div', {{ style:{{ fontFamily:"'Cormorant Garamond',serif", fontSize:20, fontWeight:500, color:"#f5f0e8", lineHeight:1.3 }} }}, "Senior Data Scientist"),
        React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:11, color:"#5a5040", marginTop:5 }} }}, "Full-time · Min. 4 years exp.")
      ),

      React.createElement('div', {{ style:{{ height:1, background:"#2a2a2a", marginBottom:28 }} }}),

      // Job Description
      React.createElement('div', {{ style:{{ marginBottom:28 }} }},
        React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.18em", marginBottom:12 }} }}, "Job Description"),
        React.createElement('p', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:11.5, color:"#6a6050", lineHeight:1.9 }} }},
          "We are looking for a Senior Data Scientist to join our AI team. You will build machine learning models, perform statistical analysis, and deploy scalable ML pipelines. Strong Python skills and experience with deep learning frameworks required."
        )
      ),

      React.createElement('div', {{ style:{{ height:1, background:"#2a2a2a", marginBottom:28 }} }}),

      // Required Skills
      React.createElement('div', {{ style:{{ marginBottom:28 }} }},
        React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.18em", marginBottom:12 }} }}, "Required Skills"),
        React.createElement('div', {{ style:{{ display:"flex", flexWrap:"wrap", gap:6 }} }},
          ...REQ.map(s => React.createElement('span', {{ key:s, style:{{ fontFamily:"'Inter',sans-serif", fontSize:10, color:"#8a7a60", border:"1px solid #2e2e2e", padding:"4px 10px", borderRadius:2, letterSpacing:"0.04em" }} }}, s))
        )
      ),

      React.createElement('div', {{ style:{{ height:1, background:"#2a2a2a", marginBottom:28 }} }}),

      // Scoring Weights
      React.createElement('div', {{ style:{{ marginBottom:28 }} }},
        React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.18em", marginBottom:14 }} }}, "Scoring Weights"),
        ...[["Semantic Fit","45%","45%"],["Skill Match","40%","40%"],["Experience","15%","15%"]].map(([l,v,w]) =>
          React.createElement('div', {{ key:l, style:{{ marginBottom:10 }} }},
            React.createElement('div', {{ style:{{ display:"flex", justifyContent:"space-between", marginBottom:5 }} }},
              React.createElement('span', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:11, color:"#5a5040" }} }}, l),
              React.createElement('span', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:11, color:"#8a7a60" }} }}, v)
            ),
            React.createElement('div', {{ style:{{ height:2, background:"#2a2a2a", borderRadius:1, overflow:"hidden" }} }},
              React.createElement('div', {{ style:{{ width:w, height:"100%", background:"#c8bea8", borderRadius:1, opacity:0.6 }} }})
            )
          )
        )
      ),

      React.createElement('div', {{ style:{{ height:1, background:"#2a2a2a", marginBottom:28 }} }}),

      // Stats grid
      React.createElement('div', {{ style:{{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14 }} }},
        ...[
          [String(DATA.length), "Candidates"],
          [String(DATA.filter(c=>c.score>=65).length), "Strong Match"],
          ["4 yrs", "Min Exp"],
          [String(REQ.length), "Skills"]
        ].map(([v,l]) =>
          React.createElement('div', {{ key:l }},
            React.createElement('div', {{ style:{{ fontFamily:"'Cormorant Garamond',serif", fontSize:24, fontWeight:500, color:"#f5f0e8", lineHeight:1 }} }}, v),
            React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.1em", marginTop:4 }} }}, l)
          )
        )
      ),

      React.createElement('div', {{ style:{{ marginTop:"auto", paddingTop:32, fontFamily:"'Inter',sans-serif", fontSize:9, color:"#333", letterSpacing:"0.1em", textTransform:"uppercase" }} }},
        "scikit-learn · TF-IDF · Python"
      )
    ),

    // ── Main Content ──
    React.createElement('div', {{ style:{{ marginLeft:300, flex:1, padding:"52px 56px" }} }},

      // Header
      React.createElement('div', {{ style:{{ marginBottom:48 }} }},
        React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.2em", marginBottom:12 }} }}, "Screening Results"),
        React.createElement('h1', {{ style:{{ fontFamily:"'Cormorant Garamond',serif", fontSize:56, fontWeight:300, color:"#1a1a1a", letterSpacing:"-1px", lineHeight:1.05 }} }},
          "Candidate", React.createElement('br'),
          React.createElement('em', {{ style:{{ fontStyle:"italic", color:"#a09070" }} }}, "Rankings")
        )
      ),

      // Candidate Cards
      ...DATA.map(c => {{
        const isOpen = open === c.rank;
        return React.createElement('div', {{ key:c.rank, style:{{ marginBottom:10 }} }},
          React.createElement('div', {{
            className:"tog",
            onClick: () => setOpen(isOpen ? null : c.rank),
            style:{{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius: isOpen ? "8px 8px 0 0" : 8, padding:"22px 26px" }}
          }},
            React.createElement('div', {{ style:{{ display:"flex", alignItems:"center", gap:18 }} }},
              React.createElement('div', {{ style:{{ flexShrink:0, textAlign:"center", width:42 }} }},
                React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#c0b8a8", letterSpacing:"0.1em" }} }}, `#${{c.rank}}`),
                React.createElement('div', {{ style:{{ width:40, height:40, borderRadius:"50%", background:"#1a1a1a", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'Cormorant Garamond',serif", fontSize:17, fontWeight:500, color:"#f5f0e8", margin:"4px auto 0" }} }}, ini(c.name))
              ),
              React.createElement('div', {{ style:{{ flex:1 }} }},
                React.createElement('div', {{ style:{{ display:"flex", alignItems:"baseline", gap:10, marginBottom:9 }} }},
                  React.createElement('span', {{ style:{{ fontFamily:"'Cormorant Garamond',serif", fontSize:28, fontWeight:500, color:"#1a1a1a" }} }}, c.name),
                  React.createElement('span', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:11, color:"#a09080" }} }}, c.fit_label)
                ),
                React.createElement('div', {{ style:{{ height:3, background:"#e8e4dc", borderRadius:2, overflow:"hidden", marginBottom:7 }} }},
                  React.createElement('div', {{ style:{{ width:`${{c.score}}%`, height:"100%", background:"#1a1a1a", opacity:0.6, borderRadius:2 }} }})
                ),
                React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:10, color:"#b0a898" }} }},
                  `${{c.matched_skills.length}}/${{REQ.length}} skills · TF-IDF ${{c.tfidf}} · Skill ${{c.skillScore}}% · ${{c.exp > 0 ? c.exp+" yrs" : "Exp N/A"}} · ${{gradeLabel(c.score)}} match`
                )
              ),
              React.createElement('div', {{ style:{{ textAlign:"right", flexShrink:0 }} }},
                React.createElement('div', {{ style:{{ fontFamily:"'Cormorant Garamond',serif", fontSize:44, fontWeight:400, color:"#1a1a1a", lineHeight:1, letterSpacing:"-1px" }} }}, c.score),
                React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#c0b8a8", marginTop:2 }} }}, "/ 100")
              ),
              React.createElement('div', {{ style:{{ color:"#c0b8a8", fontSize:11, flexShrink:0 }} }}, isOpen ? "▲" : "▼")
            )
          ),
          isOpen && React.createElement('div', {{
            style:{{ background:"#f2f0ea", border:"1px solid #ddd8ce", borderTop:"none", borderRadius:"0 0 8px 8px", padding:"22px 26px 26px" }}
          }},
            React.createElement('div', {{ style:{{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:10, marginBottom:18 }} }},
              ...[["Skill Match",`${{c.skillScore}}%`],["Semantic Fit",`${{c.tfidf}}`],["Experience", c.exp > 0 ? `${{c.exp}} yrs` : "N/A"]].map(([l,v]) =>
                React.createElement('div', {{ key:l, style:{{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius:6, padding:"12px 14px" }} }},
                  React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.14em", marginBottom:5 }} }}, l),
                  React.createElement('div', {{ style:{{ fontFamily:"'Cormorant Garamond',serif", fontSize:24, fontWeight:500, color:"#1a1a1a" }} }}, v)
                )
              )
            ),
            React.createElement('div', {{ style:{{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14 }} }},
              React.createElement('div', null,
                React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.14em", marginBottom:9 }} }}, "✓ Matched Required"),
                React.createElement('div', {{ style:{{ display:"flex", flexWrap:"wrap", gap:4 }} }},
                  ...c.matched_skills.map(s => React.createElement('span', {{ key:s, style:{{ fontFamily:"'Inter',sans-serif", fontSize:10, background:"#e8e4dc", color:"#2a2a2a", border:"1px solid #d0ccc4", padding:"3px 9px", borderRadius:2 }} }}, s))
                )
              ),
              React.createElement('div', null,
                React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.14em", marginBottom:9 }} }}, c.gaps.length ? "✗ Missing Required" : "✓ Full Coverage"),
                React.createElement('div', {{ style:{{ display:"flex", flexWrap:"wrap", gap:4 }} }},
                  c.gaps.length
                    ? c.gaps.map(s => React.createElement('span', {{ key:s, style:{{ fontFamily:"'Inter',sans-serif", fontSize:10, background:"#ede9e2", color:"#8a7a68", border:"1px solid #ccc8bc", padding:"3px 9px", borderRadius:2, textDecoration:"line-through" }} }}, s))
                    : [React.createElement('span', {{ key:"ok", style:{{ fontFamily:"'Inter',sans-serif", fontSize:12, color:"#4a4a4a" }} }}, "No gaps ✨")]
                ),
                c.pref.length > 0 && React.createElement('div', null,
                  React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.14em", margin:"12px 0 8px" }} }}, "★ Preferred Matched"),
                  React.createElement('div', {{ style:{{ display:"flex", flexWrap:"wrap", gap:4 }} }},
                    ...c.pref.map(s => React.createElement('span', {{ key:s, style:{{ fontFamily:"'Inter',sans-serif", fontSize:10, background:"#f5f2ec", color:"#6a6050", border:"1px solid #ccc8bc", padding:"3px 9px", borderRadius:2 }} }}, s))
                  )
                )
              )
            )
          )
        );
      }}),

      // Score Analysis
      React.createElement('div', {{ style:{{ marginTop:64 }} }},
        React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.2em", marginBottom:24 }} }}, "Score Analysis"),
        React.createElement('div', {{ style:{{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:14 }} }},
          ...[
            {{ title:"Overall Score (/100)", rows: DATA.map(c => ({{ name:c.name, value:c.score }})) }},
            {{ title:"Skill Match Score (%)", rows: DATA.map(c => ({{ name:c.name, value:c.skillScore }})) }},
          ].map(chart =>
            React.createElement('div', {{ key:chart.title, style:{{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius:8, padding:"22px 24px" }} }},
              React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.14em", marginBottom:18 }} }}, chart.title),
              ...chart.rows.map(({{name, value}}) =>
                React.createElement('div', {{ key:name, style:{{ display:"flex", alignItems:"center", gap:12, marginBottom:12 }} }},
                  React.createElement('div', {{ style:{{ width:30, height:30, borderRadius:"50%", background:"#1a1a1a", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'Cormorant Garamond',serif", fontSize:13, color:"#f5f0e8", flexShrink:0 }} }}, ini(name)),
                  React.createElement('div', {{ style:{{ width:82, fontFamily:"'Cormorant Garamond',serif", fontSize:15, color:"#1a1a1a", flexShrink:0 }} }}, name),
                  React.createElement('div', {{ style:{{ flex:1, height:4, background:"#e8e4dc", borderRadius:2, overflow:"hidden" }} }},
                    React.createElement('div', {{ style:{{ width:`${{value}}%`, height:"100%", background:"#1a1a1a", opacity:0.55, borderRadius:2 }} }})
                  ),
                  React.createElement('div', {{ style:{{ width:38, fontFamily:"'Inter',sans-serif", fontSize:11, fontWeight:500, color:"#4a4a4a", textAlign:"right", flexShrink:0 }} }}, value)
                )
              )
            )
          )
        ),

        // Skill Coverage vs Gaps
        React.createElement('div', {{ style:{{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius:8, padding:"22px 24px", marginBottom:14 }} }},
          React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.14em", marginBottom:18 }} }}, "Skill Coverage vs Gaps"),
          ...DATA.map(c =>
            React.createElement('div', {{ key:c.rank, style:{{ display:"flex", alignItems:"center", gap:12, marginBottom:12 }} }},
              React.createElement('div', {{ style:{{ width:30, height:30, borderRadius:"50%", background:"#1a1a1a", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'Cormorant Garamond',serif", fontSize:13, color:"#f5f0e8", flexShrink:0 }} }}, ini(c.name)),
              React.createElement('div', {{ style:{{ width:82, fontFamily:"'Cormorant Garamond',serif", fontSize:15, color:"#1a1a1a", flexShrink:0 }} }}, c.name),
              React.createElement('div', {{ style:{{ flex:1, height:10, background:"#e8e4dc", borderRadius:4, overflow:"hidden", display:"flex" }} }},
                React.createElement('div', {{ style:{{ width:`${{c.matched_skills.length*10}}%`, background:"#2a2a2a", opacity:0.6 }} }}),
                React.createElement('div', {{ style:{{ width:`${{c.gaps.length*10}}%`, background:"#a09080", opacity:0.35 }} }})
              ),
              React.createElement('div', {{ style:{{ width:120, fontFamily:"'Inter',sans-serif", fontSize:10, textAlign:"right", flexShrink:0 }} }},
                React.createElement('span', {{ style:{{ color:"#2a2a2a", fontWeight:500 }} }}, `${{c.matched_skills.length}} matched`),
                c.gaps.length > 0 && React.createElement('span', {{ style:{{ color:"#a09080", marginLeft:5 }} }}, `${{c.gaps.length}} gap${{c.gaps.length>1?"s":""}}`)
              )
            )
          ),
          React.createElement('div', {{ style:{{ display:"flex", gap:14, marginTop:12, paddingTop:12, borderTop:"1px solid #e8e4dc" }} }},
            ...[["Matched","#2a2a2a","0.6"],["Gaps","#a09080","0.35"]].map(([l,col,o]) =>
              React.createElement('div', {{ key:l, style:{{ display:"flex", alignItems:"center", gap:5, fontFamily:"'Inter',sans-serif", fontSize:9, color:"#9a9080" }} }},
                React.createElement('div', {{ style:{{ width:10, height:10, borderRadius:2, background:col, opacity:parseFloat(o) }} }}), l
              )
            )
          )
        ),

        // Skill Matrix
        React.createElement('div', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.2em", marginBottom:24, marginTop:48 }} }}, "Skill Matrix"),
        React.createElement('div', {{ style:{{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius:8, padding:"22px 24px", overflowX:"auto" }} }},
          React.createElement('table', {{ style:{{ borderCollapse:"separate", borderSpacing:5 }} }},
            React.createElement('thead', null,
              React.createElement('tr', null,
                React.createElement('th', {{ style:{{ width:110, textAlign:"left", fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", fontWeight:400, paddingBottom:10 }} }}, "Candidate"),
                ...REQ.map(s => React.createElement('th', {{ key:s, style:{{ width:28, paddingBottom:10 }} }},
                  React.createElement('div', {{ style:{{ writingMode:"vertical-rl", transform:"rotate(180deg)", height:72, display:"flex", alignItems:"center", fontFamily:"'Inter',sans-serif", fontSize:8.5, color:"#a09888", fontWeight:400 }} }}, s)
                )),
                React.createElement('th', {{ style:{{ textAlign:"center", fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", fontWeight:400, paddingLeft:12, paddingBottom:10 }} }}, "Match")
              )
            ),
            React.createElement('tbody', null,
              ...DATA.map(c =>
                React.createElement('tr', {{ key:c.rank, className:"hrow" }},
                  React.createElement('td', {{ style:{{ paddingRight:12, paddingBottom:5 }} }},
                    React.createElement('div', {{ style:{{ display:"flex", alignItems:"center", gap:7 }} }},
                      React.createElement('div', {{ style:{{ width:26, height:26, borderRadius:"50%", background:"#1a1a1a", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'Cormorant Garamond',serif", fontSize:12, color:"#f5f0e8", flexShrink:0 }} }}, ini(c.name)),
                      React.createElement('span', {{ style:{{ fontFamily:"'Cormorant Garamond',serif", fontSize:15, color:"#1a1a1a" }} }}, c.name)
                    )
                  ),
                  ...REQ.map(s => {{
                    const has = c.matched_skills.includes(s);
                    return React.createElement('td', {{ key:s, style:{{ textAlign:"center", paddingBottom:5 }} }},
                      React.createElement('div', {{ style:{{ width:24, height:24, borderRadius:4, margin:"0 auto", background: has ? "#e0dcd4" : "#f0ede6", border:`1px solid ${{has?"#c4c0b4":"#ddd8d0"}}`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:10, color: has ? "#1a1a1a" : "#c8c0b4", fontWeight:600 }} }}, has ? "✓" : "·")
                    );
                  }}),
                  React.createElement('td', {{ style:{{ paddingLeft:12, textAlign:"center", paddingBottom:5 }} }},
                    React.createElement('span', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:12, fontWeight:500, color:"#2a2a2a" }} }}, `${{Math.round(c.matched_skills.length/REQ.length*100)}}%`)
                  )
                )
              )
            )
          )
        )
      ),

      // Footer
      React.createElement('div', {{ style:{{ marginTop:64, paddingTop:22, borderTop:"1px solid #ddd8ce", display:"flex", justifyContent:"space-between" }} }},
        React.createElement('span', {{ style:{{ fontFamily:"'Cormorant Garamond',serif", fontSize:14, color:"#c0b8a8", fontStyle:"italic" }} }}, "Resume Screener · Senior Data Scientist"),
        React.createElement('span', {{ style:{{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#c0b8a8", letterSpacing:"0.1em" }} }}, "scikit-learn · TF-IDF · Python")
      )
    )
  );
}}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
</script>
</body>
</html>
"""

components.html(html, height=3200, scrolling=False)
