"""
sample_data.py — Realistic synthetic resumes + job descriptions for demo
"""

JOB_DATA_SCIENTIST = {
    "title": "Senior Data Scientist",
    "description": """
    We are looking for a Senior Data Scientist to join our AI team.
    You will build machine learning models, perform statistical analysis,
    and deploy scalable ML pipelines. The ideal candidate has strong Python
    skills, experience with deep learning frameworks, and the ability to
    communicate complex results to stakeholders.

    Responsibilities:
    - Develop and deploy machine learning and deep learning models
    - Perform exploratory data analysis and feature engineering
    - Build NLP pipelines for text classification and entity extraction
    - Collaborate with engineering to deploy models via REST APIs
    - Mentor junior data scientists

    Requirements:
    - 4+ years of experience in data science or machine learning
    - Proficiency in Python, scikit-learn, TensorFlow or PyTorch
    - Strong knowledge of statistics and algorithms
    - Experience with SQL and data manipulation using Pandas
    - Familiarity with cloud platforms (AWS, GCP, or Azure)
    """,
    "required_skills": [
        "python", "machine learning", "scikit-learn", "deep learning",
        "tensorflow", "pytorch", "statistics", "sql", "pandas", "numpy",
    ],
    "preferred_skills": [
        "nlp", "aws", "docker", "spark", "huggingface", "mlops",
        "kubernetes", "git", "flask", "fastapi",
    ],
    "min_experience_years": 4,
}

JOB_BACKEND_ENGINEER = {
    "title": "Backend Software Engineer",
    "description": """
    We need an experienced Backend Engineer to design and build scalable
    microservices. You will work with a distributed team to deliver high-quality
    APIs and integrate with cloud infrastructure.

    Responsibilities:
    - Design and build RESTful and GraphQL APIs
    - Develop microservices using Node.js or Python (FastAPI/Django)
    - Work with relational and NoSQL databases
    - Deploy and maintain services on AWS using Docker and Kubernetes
    - Participate in code reviews and agile sprints

    Requirements:
    - 3+ years of backend engineering experience
    - Strong skills in Python or JavaScript/Node.js
    - Experience with Docker, Kubernetes, and CI/CD pipelines
    - Solid understanding of REST API design
    - Knowledge of SQL (PostgreSQL) and MongoDB
    """,
    "required_skills": [
        "python", "javascript", "node.js", "rest", "api",
        "docker", "kubernetes", "sql", "postgresql", "mongodb",
    ],
    "preferred_skills": [
        "aws", "microservices", "django", "fastapi", "redis",
        "kafka", "ci/cd", "git", "agile", "scrum",
    ],
    "min_experience_years": 3,
}

# ── Sample Resumes ────────────────────────────────────────────────────────────

RESUMES = [
    {
        "name": "Alice Chen",
        "text": """
Alice Chen | alice@email.com | linkedin.com/in/alicechen

SUMMARY
Data scientist with 6 years of experience building end-to-end machine learning
solutions. Passionate about NLP and computer vision applications.

SKILLS
Python, TensorFlow, PyTorch, scikit-learn, pandas, numpy, SQL, Spark,
Docker, AWS, MLOps, Huggingface, FastAPI, Git, Statistics, Algorithms

EXPERIENCE
Senior Data Scientist – TechCorp (2020 – 2024)
- Built deep learning NLP models achieving 93% accuracy on classification tasks
- Deployed machine learning models on AWS using Docker and Kubernetes
- Led a team of 3 junior data scientists; mentored on best practices
- Designed REST API endpoints using FastAPI for model serving

Data Scientist – DataLabs Inc (2018 – 2020)
- Performed feature engineering and statistical analysis on large datasets
- Used scikit-learn and XGBoost for predictive modelling
- Developed automated data pipelines using Python and Spark

EDUCATION
M.Sc. Computer Science (Machine Learning), Stanford University, 2018
B.Sc. Mathematics, MIT, 2016

CERTIFICATIONS
AWS Certified Machine Learning Specialist (2022)
Google Professional Data Engineer (2021)
        """
    },
    {
        "name": "Bob Martinez",
        "text": """
Bob Martinez | bob@email.com

OBJECTIVE
Passionate junior data scientist seeking to grow in an ML-focused environment.

SKILLS
Python, pandas, numpy, matplotlib, scikit-learn, SQL, Git, Excel, Tableau

EXPERIENCE
Data Analyst – RetailCo (2022 – 2024)
- Analysed sales data using Python and pandas; created dashboards in Tableau
- Applied basic regression and classification models with scikit-learn
- Wrote SQL queries to extract and clean data from PostgreSQL

Intern – AnalyticsFirm (2021 – 2022)
- Assisted with data cleaning and exploratory analysis
- Visualised results using matplotlib and seaborn

EDUCATION
B.Sc. Statistics, UCLA, 2021

PROJECTS
Customer Churn Prediction – scikit-learn, pandas, matplotlib
House Price Regression – Python, numpy, statsmodels
        """
    },
    {
        "name": "Carol Nguyen",
        "text": """
Carol Nguyen | carol.nguyen@email.com | github.com/caroln

PROFILE
Full-stack engineer transitioning into ML engineering. Strong Python background
with 5 years of backend development and growing expertise in deep learning.

TECHNICAL SKILLS
Python, JavaScript, Node.js, FastAPI, Django, Docker, Kubernetes, AWS, GCP,
PostgreSQL, MongoDB, Redis, TensorFlow, Keras, scikit-learn, pandas, Git,
CI/CD, Microservices, REST, API, Agile, Scrum

EXPERIENCE
Senior Backend Engineer – CloudApps (2019 – 2024)
- Architected microservices in Python/FastAPI deployed on AWS via Kubernetes
- Integrated MongoDB and PostgreSQL for data storage; Redis for caching
- Built CI/CD pipelines using Jenkins and GitHub Actions

ML Side Projects (2022 – 2024)
- Trained text classification models using TensorFlow and Huggingface
- Fine-tuned BERT for sentiment analysis on 500K reviews (88% accuracy)
- Deployed model as REST API on AWS Lambda

EDUCATION
B.Eng. Software Engineering, Georgia Tech, 2019
        """
    },
    {
        "name": "David Okafor",
        "text": """
David Okafor

SKILLS
Java, Spring, MySQL, Git, Linux, Agile

EXPERIENCE
Java Developer – SoftHouse Ltd (2021 – 2023)
- Built enterprise applications using Java and Spring Boot
- Managed MySQL databases and wrote complex SQL queries

EDUCATION
B.Sc. Computer Science, University of Lagos, 2020
        """
    },
    {
        "name": "Eva Schmidt",
        "text": """
Eva Schmidt | eva.schmidt@email.com

SUMMARY
PhD-level researcher specialising in NLP and statistical modelling with
4 years of combined academic and industry experience.

SKILLS
Python, R, NLTK, spaCy, Huggingface, Transformers, PyTorch, scikit-learn,
statistics, machine learning, deep learning, algorithms, data structures,
pandas, numpy, SQL, Git, Tableau, Matplotlib

EXPERIENCE
NLP Research Scientist – AI Lab Berlin (2022 – 2024)
- Published 3 papers on transformer-based language models
- Implemented state-of-the-art NLP models using PyTorch and Huggingface
- Collaborated with product team to ship NLP features in production

Research Assistant – TU Berlin (2020 – 2022)
- Applied statistical analysis and machine learning to medical datasets
- Developed Python pipelines for data preprocessing and model evaluation

EDUCATION
PhD Computational Linguistics, TU Berlin, 2022 (expected)
M.Sc. Data Science, Humboldt University, 2019
B.Sc. Mathematics, Freie Universität Berlin, 2017
        """
    },
]
