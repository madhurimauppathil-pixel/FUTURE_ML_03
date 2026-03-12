import { useState } from "react";

// ── Real data from resume_screener.py + sample_data.py ──
const DATA = [
  {
    rank: 1, name: "Alice Chen",  title: "Sr. Data Scientist", score: 68.00, grade: "B+",
    tfidf: 31.55, skillScore: 97, expScore: 100, exp: 6.0,
    matched: 10, total: 10, gapCount: 0,
    matched_skills: ["deep learning","machine learning","numpy","pandas","python","pytorch","scikit-learn","sql","statistics","tensorflow"],
    gaps: [],
    pref: ["aws","docker","fastapi","git","huggingface","kubernetes","mlops","nlp","spark"],
  },
  {
    rank: 2, name: "Eva Schmidt", title: "NLP Researcher",     score: 39.15, grade: "D",
    tfidf: 19.66, skillScore: 72, expScore: 10, exp: 0.0,
    matched: 9, total: 10, gapCount: 1,
    matched_skills: ["deep learning","machine learning","numpy","pandas","python","pytorch","scikit-learn","sql","statistics"],
    gaps: ["tensorflow"],
    pref: ["git","huggingface","nlp"],
  },
  {
    rank: 3, name: "Carol Nguyen",title: "Backend Engineer",   score: 28.40, grade: "D",
    tfidf: 12.66, skillScore: 53, expScore: 10, exp: 0.0,
    matched: 5, total: 10, gapCount: 5,
    matched_skills: ["deep learning","pandas","python","scikit-learn","tensorflow"],
    gaps: ["machine learning","numpy","pytorch","sql","statistics"],
    pref: ["aws","docker","fastapi","git","huggingface","kubernetes"],
  },
  {
    rank: 4, name: "Bob Martinez", title: "Data Analyst",      score: 26.28, grade: "D",
    tfidf: 15.07, skillScore: 45, expScore: 10, exp: 0.0,
    matched: 6, total: 10, gapCount: 4,
    matched_skills: ["numpy","pandas","python","scikit-learn","sql","statistics"],
    gaps: ["deep learning","machine learning","pytorch","tensorflow"],
    pref: ["git"],
  },
  {
    rank: 5, name: "David Okafor",title: "Java Developer",     score: 6.74,  grade: "D",
    tfidf: 2.76, skillScore: 10, expScore: 10, exp: 0.0,
    matched: 1, total: 10, gapCount: 9,
    matched_skills: ["sql"],
    gaps: ["deep learning","machine learning","numpy","pandas","python","pytorch","scikit-learn","statistics","tensorflow"],
    pref: ["git"],
  },
];

const REQ = ["python","machine learning","scikit-learn","deep learning","tensorflow","pytorch","statistics","sql","pandas","numpy"];
const JD = `We are looking for a Senior Data Scientist to join our AI team. You will build machine learning models, perform statistical analysis, and deploy scalable ML pipelines. The ideal candidate has strong Python skills, experience with deep learning frameworks, and the ability to communicate complex results to stakeholders.`;

const ini = n => n.split(" ").map(w=>w[0]).join("");
const fitLabel = s => s >= 65 ? "Strong Match" : s >= 45 ? "Moderate Match" : "Weak Match";

export default function App() {
  const [open, setOpen] = useState(null);

  return (
    <div style={{ display:"flex", minHeight:"100vh", fontFamily:"Georgia,serif", color:"#1a1a1a", background:"#f7f5f0" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500&display=swap');
        * { box-sizing:border-box; margin:0; padding:0; }
        ::-webkit-scrollbar { width:4px; }
        ::-webkit-scrollbar-thumb { background:#3a3a3a; border-radius:4px; }
        .tog { cursor:pointer; transition:background 0.15s; }
        .tog:hover { background:#f0ede6 !important; }
        .hrow:hover { background:#f0ede6 !important; }
      `}</style>

      {/* ── Fixed Left Sidebar ── */}
      <div style={{ width:290, background:"#1a1a1a", position:"fixed", top:0, left:0, height:"100vh", overflowY:"auto", display:"flex", flexDirection:"column", padding:"44px 32px", flexShrink:0 }}>

        <div style={{ marginBottom:30 }}>
          <div style={{ fontFamily:"'Cormorant Garamond',serif", fontSize:21, fontWeight:500, color:"#f5f0e8", marginBottom:4 }}>Resume Screener</div>
          <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", letterSpacing:"0.18em", textTransform:"uppercase" }}>Candidate Analysis · 2025</div>
        </div>

        <div style={{ height:1, background:"#252525", marginBottom:26 }} />

        <div style={{ marginBottom:22 }}>
          <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.16em", marginBottom:8 }}>Role</div>
          <div style={{ fontFamily:"'Cormorant Garamond',serif", fontSize:19, fontWeight:500, color:"#f5f0e8" }}>Senior Data Scientist</div>
          <div style={{ fontFamily:"'Inter',sans-serif", fontSize:11, color:"#5a5040", marginTop:4 }}>Full-time · Min. 4 years</div>
        </div>

        <div style={{ height:1, background:"#252525", marginBottom:26 }} />

        <div style={{ marginBottom:22 }}>
          <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.16em", marginBottom:10 }}>Job Description</div>
          <p style={{ fontFamily:"'Inter',sans-serif", fontSize:11, color:"#5a5040", lineHeight:1.85 }}>{JD}</p>
        </div>

        <div style={{ height:1, background:"#252525", marginBottom:26 }} />

        <div style={{ marginBottom:22 }}>
          <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.16em", marginBottom:10 }}>Required Skills</div>
          <div style={{ display:"flex", flexWrap:"wrap", gap:5 }}>
            {REQ.map(s => (
              <span key={s} style={{ fontFamily:"'Inter',sans-serif", fontSize:9.5, color:"#7a6a58", border:"1px solid #2e2e2e", padding:"3px 9px", borderRadius:2, letterSpacing:"0.04em" }}>{s}</span>
            ))}
          </div>
        </div>

        <div style={{ height:1, background:"#252525", marginBottom:26 }} />

        <div style={{ marginBottom:26 }}>
          <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.16em", marginBottom:12 }}>Scoring Weights</div>
          {[["Semantic Fit","45%","45%"],["Skill Match","40%","40%"],["Experience","15%","15%"]].map(([l,v,w]) => (
            <div key={l} style={{ marginBottom:9 }}>
              <div style={{ display:"flex", justifyContent:"space-between", marginBottom:4 }}>
                <span style={{ fontFamily:"'Inter',sans-serif", fontSize:10.5, color:"#5a5040" }}>{l}</span>
                <span style={{ fontFamily:"'Inter',sans-serif", fontSize:10.5, color:"#8a7a60" }}>{v}</span>
              </div>
              <div style={{ height:2, background:"#2a2a2a", borderRadius:1, overflow:"hidden" }}>
                <div style={{ width:w, height:"100%", background:"#c8bea8", opacity:0.5 }} />
              </div>
            </div>
          ))}
        </div>

        <div style={{ height:1, background:"#252525", marginBottom:26 }} />

        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14 }}>
          {[["5","Candidates"],["1","Strong Match"],["4 yrs","Min Exp"],["10","Skills Req."]].map(([v,l]) => (
            <div key={l}>
              <div style={{ fontFamily:"'Cormorant Garamond',serif", fontSize:26, fontWeight:500, color:"#f5f0e8", lineHeight:1 }}>{v}</div>
              <div style={{ fontFamily:"'Inter',sans-serif", fontSize:8.5, color:"#4a4040", textTransform:"uppercase", letterSpacing:"0.1em", marginTop:4 }}>{l}</div>
            </div>
          ))}
        </div>

        <div style={{ marginTop:"auto", paddingTop:28, fontFamily:"'Inter',sans-serif", fontSize:8.5, color:"#2e2e2e", letterSpacing:"0.1em" }}>
          scikit-learn · TF-IDF · Python
        </div>
      </div>

      {/* ── Right Scrollable Content ── */}
      <div style={{ marginLeft:290, flex:1, padding:"48px 52px" }}>

        {/* Page heading */}
        <div style={{ marginBottom:44 }}>
          <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.2em", marginBottom:10 }}>Screening Results</div>
          <h1 style={{ fontFamily:"'Cormorant Garamond',serif", fontSize:52, fontWeight:300, color:"#1a1a1a", letterSpacing:"-1px", lineHeight:1.05 }}>
            Candidate<br /><em style={{ fontStyle:"italic", color:"#a09070" }}>Rankings</em>
          </h1>
        </div>

        {/* ── Candidate Cards ── */}
        {DATA.map((c) => {
          const isOpen = open === c.rank;
          return (
            <div key={c.rank} style={{ marginBottom:10 }}>
              <div className="tog" onClick={() => setOpen(isOpen ? null : c.rank)}
                style={{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius: isOpen ? "8px 8px 0 0" : 8, padding:"20px 24px" }}>
                <div style={{ display:"flex", alignItems:"center", gap:16 }}>
                  <div style={{ flexShrink:0, textAlign:"center", width:40 }}>
                    <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#c0b8a8", letterSpacing:"0.08em" }}>#{c.rank}</div>
                    <div style={{ width:38, height:38, borderRadius:"50%", background:"#1a1a1a", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'Cormorant Garamond',serif", fontSize:13, fontWeight:500, color:"#f5f0e8", margin:"4px auto 0" }}>{ini(c.name)}</div>
                  </div>
                  <div style={{ flex:1 }}>
                    <div style={{ display:"flex", alignItems:"baseline", gap:10, marginBottom:8 }}>
                      <span style={{ fontFamily:"'Cormorant Garamond',serif", fontSize:26, fontWeight:500, color:"#1a1a1a" }}>{c.name}</span>
                      <span style={{ fontFamily:"'Inter',sans-serif", fontSize:10.5, color:"#a09080" }}>{c.title}</span>
                      <span style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#c0b8a8", marginLeft:"auto" }}>Grade: {c.grade} · {fitLabel(c.score)}</span>
                    </div>
                    <div style={{ height:3, background:"#e8e4dc", borderRadius:2, overflow:"hidden", marginBottom:6 }}>
                      <div style={{ width:`${c.score}%`, height:"100%", background:"#1a1a1a", opacity:0.6, borderRadius:2 }} />
                    </div>
                    <div style={{ fontFamily:"'Inter',sans-serif", fontSize:10, color:"#b0a898" }}>
                      {c.matched}/{c.total} required &nbsp;·&nbsp; TF-IDF {c.tfidf}% &nbsp;·&nbsp; Skill {c.skillScore}% &nbsp;·&nbsp; {c.exp > 0 ? `${c.exp} yrs` : "Exp not detected"}
                    </div>
                  </div>
                  <div style={{ textAlign:"right", flexShrink:0 }}>
                    <div style={{ fontFamily:"'Cormorant Garamond',serif", fontSize:42, fontWeight:400, color:"#1a1a1a", lineHeight:1, letterSpacing:"-1px" }}>{c.score.toFixed(2)}</div>
                    <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#c0b8a8", marginTop:2 }}>/ 100</div>
                  </div>
                  <div style={{ color:"#c0b8a8", fontSize:10, flexShrink:0 }}>{isOpen ? "▲" : "▼"}</div>
                </div>
              </div>

              {isOpen && (
                <div style={{ background:"#f2f0ea", border:"1px solid #ddd8ce", borderTop:"none", borderRadius:"0 0 8px 8px", padding:"20px 24px 24px" }}>
                  <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:10, marginBottom:16 }}>
                    {[
                      ["Skill Score", `${c.skillScore}%`],
                      ["Semantic",    `${c.tfidf}%`],
                      ["Experience",  c.exp > 0 ? `${c.exp} yrs` : "—"],
                      ["Gaps",        c.gapCount],
                    ].map(([l,v]) => (
                      <div key={l} style={{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius:6, padding:"11px 13px" }}>
                        <div style={{ fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.12em", marginBottom:5 }}>{l}</div>
                        <div style={{ fontFamily:"'Cormorant Garamond',serif", fontSize:22, fontWeight:500, color:"#1a1a1a" }}>{v}</div>
                      </div>
                    ))}
                  </div>
                  <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14 }}>
                    <div>
                      <div style={{ fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.12em", marginBottom:8 }}>✓ Matched</div>
                      <div style={{ display:"flex", flexWrap:"wrap", gap:4 }}>
                        {c.matched_skills.map(s => <span key={s} style={{ fontFamily:"'Inter',sans-serif", fontSize:9.5, background:"#e8e4dc", color:"#2a2a2a", border:"1px solid #d0ccc4", padding:"3px 8px", borderRadius:2 }}>{s}</span>)}
                      </div>
                    </div>
                    <div>
                      <div style={{ fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.12em", marginBottom:8 }}>
                        {c.gaps.length ? "✗ Missing" : "✓ No Gaps"}
                      </div>
                      <div style={{ display:"flex", flexWrap:"wrap", gap:4 }}>
                        {c.gaps.length
                          ? c.gaps.map(s => <span key={s} style={{ fontFamily:"'Inter',sans-serif", fontSize:9.5, background:"#ede9e2", color:"#8a7a68", border:"1px solid #ccc8bc", padding:"3px 8px", borderRadius:2, textDecoration:"line-through" }}>{s}</span>)
                          : <span style={{ fontFamily:"'Inter',sans-serif", fontSize:12, color:"#4a4a4a" }}>Perfect coverage ✨</span>
                        }
                      </div>
                      {c.pref.length > 0 && <>
                        <div style={{ fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.12em", margin:"12px 0 8px" }}>★ Preferred Matched</div>
                        <div style={{ display:"flex", flexWrap:"wrap", gap:4 }}>
                          {c.pref.map(s => <span key={s} style={{ fontFamily:"'Inter',sans-serif", fontSize:9.5, background:"#f5f2ec", color:"#6a6050", border:"1px solid #ccc8bc", padding:"3px 8px", borderRadius:2 }}>{s}</span>)}
                        </div>
                      </>}
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}

        {/* ── Score Analysis ── */}
        <div style={{ marginTop:60 }}>
          <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.2em", marginBottom:22 }}>Score Analysis</div>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:14 }}>
            {[
              { title:"Overall Score",  rows: DATA.map(c => ({ name:c.name, value:c.score, display: c.score.toFixed(2) })) },
              { title:"Skill Match %",  rows: DATA.map(c => ({ name:c.name, value:c.skillScore, display: `${c.skillScore}%` })) },
            ].map(chart => (
              <div key={chart.title} style={{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius:8, padding:"20px 22px" }}>
                <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.12em", marginBottom:16 }}>{chart.title}</div>
                {chart.rows.map(({ name, value, display }) => (
                  <div key={name} style={{ display:"flex", alignItems:"center", gap:12, marginBottom:11 }}>
                    <div style={{ width:28, height:28, borderRadius:"50%", background:"#1a1a1a", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'Cormorant Garamond',serif", fontSize:11, color:"#f5f0e8", flexShrink:0 }}>{ini(name)}</div>
                    <div style={{ width:88, fontFamily:"'Cormorant Garamond',serif", fontSize:15, color:"#1a1a1a", flexShrink:0 }}>{name}</div>
                    <div style={{ flex:1, height:4, background:"#e8e4dc", borderRadius:2, overflow:"hidden" }}>
                      <div style={{ width:`${value}%`, height:"100%", background:"#1a1a1a", opacity:0.55 }} />
                    </div>
                    <div style={{ width:40, fontFamily:"'Inter',sans-serif", fontSize:10.5, fontWeight:500, color:"#4a4a4a", textAlign:"right", flexShrink:0 }}>{display}</div>
                  </div>
                ))}
              </div>
            ))}
          </div>

          <div style={{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius:8, padding:"20px 22px" }}>
            <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.12em", marginBottom:16 }}>Coverage vs Gaps</div>
            {DATA.map(c => (
              <div key={c.rank} style={{ display:"flex", alignItems:"center", gap:12, marginBottom:11 }}>
                <div style={{ width:28, height:28, borderRadius:"50%", background:"#1a1a1a", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'Cormorant Garamond',serif", fontSize:11, color:"#f5f0e8", flexShrink:0 }}>{ini(c.name)}</div>
                <div style={{ width:88, fontFamily:"'Cormorant Garamond',serif", fontSize:15, color:"#1a1a1a", flexShrink:0 }}>{c.name}</div>
                <div style={{ flex:1, height:10, background:"#e8e4dc", borderRadius:4, overflow:"hidden", display:"flex" }}>
                  <div style={{ width:`${(c.matched/10)*100}%`, background:"#2a2a2a", opacity:0.6 }} />
                  <div style={{ width:`${(c.gapCount/10)*100}%`, background:"#a09080", opacity:0.35 }} />
                </div>
                <div style={{ width:110, fontFamily:"'Inter',sans-serif", fontSize:10, textAlign:"right", flexShrink:0 }}>
                  <span style={{ color:"#2a2a2a", fontWeight:500 }}>{c.matched} matched</span>
                  {c.gapCount > 0 && <span style={{ color:"#a09080", marginLeft:5 }}>{c.gapCount} gap{c.gapCount > 1 ? "s":""}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ── Skill Matrix ── */}
        <div style={{ marginTop:60 }}>
          <div style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#b0a898", textTransform:"uppercase", letterSpacing:"0.2em", marginBottom:22 }}>Skill Matrix</div>
          <div style={{ background:"#faf8f4", border:"1px solid #ddd8ce", borderRadius:8, padding:"20px 22px", overflowX:"auto" }}>
            <table style={{ borderCollapse:"separate", borderSpacing:4 }}>
              <thead>
                <tr>
                  <th style={{ width:110, textAlign:"left", fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", fontWeight:400, paddingBottom:10 }}>Candidate</th>
                  {REQ.map(s => (
                    <th key={s} style={{ width:28, paddingBottom:10 }}>
                      <div style={{ writingMode:"vertical-rl", transform:"rotate(180deg)", height:70, display:"flex", alignItems:"center", fontFamily:"'Inter',sans-serif", fontSize:8.5, color:"#a09888", fontWeight:400 }}>{s}</div>
                    </th>
                  ))}
                  <th style={{ textAlign:"center", fontFamily:"'Inter',sans-serif", fontSize:8, color:"#b0a898", fontWeight:400, paddingLeft:12, paddingBottom:10 }}>Match</th>
                </tr>
              </thead>
              <tbody>
                {DATA.map(c => (
                  <tr key={c.rank} className="hrow" style={{ background:"transparent", transition:"background 0.12s" }}>
                    <td style={{ paddingRight:10, paddingBottom:5 }}>
                      <div style={{ display:"flex", alignItems:"center", gap:7 }}>
                        <div style={{ width:24, height:24, borderRadius:"50%", background:"#1a1a1a", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'Cormorant Garamond',serif", fontSize:10, color:"#f5f0e8", flexShrink:0 }}>{ini(c.name)}</div>
                        <span style={{ fontFamily:"'Cormorant Garamond',serif", fontSize:15, color:"#1a1a1a" }}>{c.name}</span>
                      </div>
                    </td>
                    {REQ.map(s => {
                      const has = c.matched_skills.includes(s);
                      return (
                        <td key={s} style={{ textAlign:"center", paddingBottom:5 }}>
                          <div style={{ width:24, height:24, borderRadius:4, margin:"0 auto", background: has ? "#e0dcd4" : "#f0ede6", border:`1px solid ${has?"#c4c0b4":"#ddd8d0"}`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:10, color: has ? "#1a1a1a" : "#c8c0b4", fontWeight:600 }}>
                            {has ? "✓" : "·"}
                          </div>
                        </td>
                      );
                    })}
                    <td style={{ paddingLeft:12, textAlign:"center", paddingBottom:5 }}>
                      <span style={{ fontFamily:"'Inter',sans-serif", fontSize:11.5, fontWeight:500, color:"#2a2a2a" }}>{Math.round(c.matched/10*100)}%</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Footer */}
        <div style={{ marginTop:60, paddingTop:20, borderTop:"1px solid #ddd8ce", display:"flex", justifyContent:"space-between" }}>
          <span style={{ fontFamily:"'Cormorant Garamond',serif", fontSize:13, color:"#c0b8a8", fontStyle:"italic" }}>Resume Screener</span>
          <span style={{ fontFamily:"'Inter',sans-serif", fontSize:9, color:"#c0b8a8", letterSpacing:"0.1em" }}>scikit-learn · TF-IDF · Python</span>
        </div>

      </div>
    </div>
  );
}
