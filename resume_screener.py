"""
Resume / Candidate Screening System
FUTURE_ML_TaskNumber: FUTURE_ML_03
Tools: Python (spaCy / NLTK), Scikit-learn
"""

import re
import json
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

# ── NLP imports (graceful fallback) ──────────────────────────────────────────
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    NLP_BACKEND = "spacy"
except Exception:
    try:
        import nltk
        for pkg in ["punkt", "stopwords", "averaged_perceptron_tagger", "wordnet"]:
            try:
                nltk.download(pkg, quiet=True)
            except Exception:
                pass
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from nltk.stem import WordNetLemmatizer
        NLP_BACKEND = "nltk"
    except Exception:
        NLP_BACKEND = "basic"

print(f"[INFO] NLP Backend: {NLP_BACKEND}")


# ─────────────────────────────────────────────────────────────────────────────
# 1. TEXT CLEANING & PARSING
# ─────────────────────────────────────────────────────────────────────────────

class ResumeParser:
    """Clean and extract structured information from raw resume text."""

    SECTION_HEADERS = {
        "skills":      r"(skills?|technical\s+skills?|core\s+competencies|proficiencies)",
        "experience":  r"(experience|work\s+history|employment|professional\s+background)",
        "education":   r"(education|academic|qualification|degree)",
        "projects":    r"(projects?|portfolio|work\s+samples?)",
        "certifications": r"(certif|license|credential|course)",
        "summary":     r"(summary|objective|profile|about)",
    }

    SKILL_PATTERNS = [
        # Programming languages
        r"\b(python|java|javascript|typescript|c\+\+|c#|go|rust|ruby|php|swift|kotlin|scala|r|matlab)\b",
        # Web / frameworks
        r"\b(react|angular|vue|django|flask|fastapi|spring|node\.?js|express|laravel|rails)\b",
        # Data / ML
        r"\b(tensorflow|pytorch|keras|scikit[\-\s]?learn|pandas|numpy|scipy|matplotlib|seaborn|"
        r"opencv|nltk|spacy|huggingface|transformers|xgboost|lightgbm|sklearn)\b",
        # Cloud / DevOps
        r"\b(aws|azure|gcp|docker|kubernetes|jenkins|terraform|ansible|ci/cd|devops|mlops)\b",
        # Databases
        r"\b(sql|mysql|postgresql|mongodb|redis|cassandra|elasticsearch|oracle|sqlite|neo4j)\b",
        # Tools
        r"\b(git|github|gitlab|jira|confluence|tableau|power\s?bi|excel|spark|hadoop|kafka)\b",
        # Concepts
        r"\b(machine\s+learning|deep\s+learning|nlp|computer\s+vision|data\s+science|"
        r"statistics|algorithms?|data\s+structures?|oop|agile|scrum|rest|api|microservices)\b",
    ]

    def __init__(self):
        self.skill_regex = re.compile(
            "|".join(self.SKILL_PATTERNS), re.IGNORECASE
        )

    def clean_text(self, text: str) -> str:
        """Remove noise while preserving meaningful content."""
        text = re.sub(r"[^\x00-\x7F]+", " ", text)        # non-ASCII
        text = re.sub(r"\s+", " ", text)                   # whitespace
        text = re.sub(r"[^\w\s\.\,\-\+\#\/]", " ", text)  # special chars
        return text.strip()

    def extract_sections(self, text: str) -> dict:
        """Split resume into labelled sections."""
        sections = defaultdict(str)
        lines = text.split("\n")
        current_section = "general"

        for line in lines:
            line_lower = line.lower().strip()
            matched = False
            for sec_name, pattern in self.SECTION_HEADERS.items():
                if re.search(pattern, line_lower):
                    current_section = sec_name
                    matched = True
                    break
            if not matched:
                sections[current_section] += " " + line

        return dict(sections)

    def extract_skills(self, text: str) -> list:
        """Extract technology / skill mentions from text."""
        matches = self.skill_regex.findall(text.lower())
        # flatten groups from alternation
        skills = []
        for m in matches:
            if isinstance(m, tuple):
                skills.extend([s for s in m if s])
            else:
                skills.append(m)
        # normalise
        skills = [re.sub(r"\s+", " ", s.strip()) for s in skills]
        return sorted(set(skills))

    def extract_experience_years(self, text: str) -> float:
        """Heuristically estimate total years of experience."""
        patterns = [
            r"(\d+)\+?\s*years?\s+of\s+experience",
            r"(\d+)\+?\s*years?\s+experience",
            r"experience\s+of\s+(\d+)\+?\s*years?",
        ]
        years = []
        for pat in patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                years.append(float(m.group(1)))
        # date range pattern: 2019 – 2023
        date_ranges = re.findall(
            r"\b(20\d{2}|19\d{2})\s*[-–—to]+\s*(20\d{2}|19\d{2}|present|current|now)\b",
            text, re.IGNORECASE
        )
        current_year = 2024
        for start, end in date_ranges:
            try:
                s = int(start)
                e = current_year if end.lower() in ("present", "current", "now") else int(end)
                years.append(max(0, e - s))
            except ValueError:
                pass
        return round(sum(years) / max(len(years), 1), 1) if years else 0.0

    def parse(self, text: str, name: str = "Candidate") -> dict:
        """Full parse pipeline for a single resume."""
        clean = self.clean_text(text)
        sections = self.extract_sections(clean)
        skills = self.extract_skills(clean)
        exp_years = self.extract_experience_years(clean)
        word_count = len(clean.split())

        return {
            "name": name,
            "raw_text": text,
            "clean_text": clean,
            "sections": sections,
            "skills": skills,
            "experience_years": exp_years,
            "word_count": word_count,
        }


# ─────────────────────────────────────────────────────────────────────────────
# 2. SCORING ENGINE
# ─────────────────────────────────────────────────────────────────────────────

class ScoringEngine:
    """
    Scores a parsed resume against a job description using:
      • TF-IDF cosine similarity   (semantic relevance)
      • Skill match ratio          (hard-skill coverage)
      • Experience bonus           (years threshold)
    """

    WEIGHTS = {
        "tfidf_similarity": 0.45,
        "skill_match":      0.40,
        "experience_bonus": 0.15,
    }

    def __init__(self):
        self.parser = ResumeParser()
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
            max_features=5000,
        )

    def _tfidf_score(self, resume_text: str, jd_text: str) -> float:
        try:
            matrix = self.vectorizer.fit_transform([jd_text, resume_text])
            sim = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
            return float(sim)
        except Exception:
            return 0.0

    def _skill_score(self, resume_skills: list, required_skills: list,
                     preferred_skills: list) -> tuple:
        resume_set = set(s.lower() for s in resume_skills)
        req_set    = set(s.lower() for s in required_skills)
        pref_set   = set(s.lower() for s in preferred_skills)

        matched_req  = resume_set & req_set
        matched_pref = resume_set & pref_set
        missing_req  = req_set - resume_set
        missing_pref = pref_set - resume_set

        req_ratio  = len(matched_req)  / max(len(req_set), 1)
        pref_ratio = len(matched_pref) / max(len(pref_set), 1)
        combined   = 0.7 * req_ratio + 0.3 * pref_ratio

        return (
            round(combined, 4),
            sorted(matched_req), sorted(matched_pref),
            sorted(missing_req), sorted(missing_pref),
        )

    def _experience_score(self, years: float, min_years: float) -> float:
        if min_years <= 0:
            return 1.0
        ratio = years / min_years
        if ratio >= 1.0:
            return 1.0
        elif ratio >= 0.75:
            return 0.7
        elif ratio >= 0.5:
            return 0.4
        else:
            return 0.1

    def score(self, parsed_resume: dict, job: dict) -> dict:
        """
        Returns a detailed score dict for one resume against one job.
        `job` must have keys: description, required_skills, preferred_skills,
                               min_experience_years
        """
        tfidf = self._tfidf_score(
            parsed_resume["clean_text"], job["description"]
        )
        skill_score, m_req, m_pref, miss_req, miss_pref = self._skill_score(
            parsed_resume["skills"],
            job.get("required_skills", []),
            job.get("preferred_skills", []),
        )
        exp_score = self._experience_score(
            parsed_resume["experience_years"],
            job.get("min_experience_years", 0),
        )

        total = (
            self.WEIGHTS["tfidf_similarity"] * tfidf
            + self.WEIGHTS["skill_match"]      * skill_score
            + self.WEIGHTS["experience_bonus"] * exp_score
        )

        return {
            "name":               parsed_resume["name"],
            "total_score":        round(total * 100, 2),
            "tfidf_similarity":   round(tfidf * 100, 2),
            "skill_match_score":  round(skill_score * 100, 2),
            "experience_score":   round(exp_score * 100, 2),
            "experience_years":   parsed_resume["experience_years"],
            "matched_required":   m_req,
            "matched_preferred":  m_pref,
            "missing_required":   miss_req,
            "missing_preferred":  miss_pref,
            "total_skills_found": len(parsed_resume["skills"]),
            "skill_gap_count":    len(miss_req),
        }


# ─────────────────────────────────────────────────────────────────────────────
# 3. RANKING & REPORTING
# ─────────────────────────────────────────────────────────────────────────────

class ResumeScreener:
    """High-level API: accepts resumes + job description, returns ranked results."""

    GRADE_MAP = [
        (85, "A+", "Excellent Match"),
        (75, "A",  "Strong Match"),
        (65, "B+", "Good Match"),
        (55, "B",  "Moderate Match"),
        (40, "C",  "Weak Match"),
        ( 0, "D",  "Poor Match"),
    ]

    def __init__(self):
        self.parser  = ResumeParser()
        self.engine  = ScoringEngine()

    def _grade(self, score: float) -> tuple:
        for threshold, grade, label in self.GRADE_MAP:
            if score >= threshold:
                return grade, label
        return "D", "Poor Match"

    def screen(self, resumes: list[dict], job: dict) -> pd.DataFrame:
        """
        Parameters
        ----------
        resumes : list of {"name": str, "text": str}
        job     : {"title": str, "description": str,
                   "required_skills": list, "preferred_skills": list,
                   "min_experience_years": float}

        Returns
        -------
        pandas DataFrame sorted by total_score descending
        """
        results = []
        for r in resumes:
            parsed = self.parser.parse(r["text"], r.get("name", "Unknown"))
            scored = self.engine.score(parsed, job)
            grade, label = self._grade(scored["total_score"])
            scored["grade"] = grade
            scored["fit_label"] = label
            results.append(scored)

        df = pd.DataFrame(results).sort_values(
            "total_score", ascending=False
        ).reset_index(drop=True)
        df.index += 1          # 1-based rank
        df.index.name = "rank"
        return df

    def report(self, df: pd.DataFrame, job_title: str = "Role") -> str:
        """Pretty-print a summary report."""
        lines = [
            "=" * 65,
            f"  CANDIDATE SCREENING REPORT — {job_title.upper()}",
            "=" * 65,
        ]
        for rank, row in df.iterrows():
            lines += [
                f"\n  #{rank}  {row['name']}",
                f"      Overall Score : {row['total_score']:.1f}/100  [{row['grade']}] {row['fit_label']}",
                f"      Semantic Sim  : {row['tfidf_similarity']:.1f}  |  "
                f"Skill Match : {row['skill_match_score']:.1f}  |  "
                f"Experience  : {row['experience_years']} yrs",
                f"      Skills Found  : {row['total_skills_found']}  |  "
                f"Skill Gaps : {row['skill_gap_count']}",
            ]
            if row["matched_required"]:
                lines.append(f"      ✓ Required    : {', '.join(row['matched_required'])}")
            if row["missing_required"]:
                lines.append(f"      ✗ Missing Req : {', '.join(row['missing_required'])}")
            if row["matched_preferred"]:
                lines.append(f"      ★ Preferred   : {', '.join(row['matched_preferred'])}")
        lines.append("\n" + "=" * 65)
        return "\n".join(lines)
