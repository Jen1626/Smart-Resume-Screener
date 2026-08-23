# Smart Resume Screener

AI-powered resume parsing, semantic job matching, and candidate ranking using Google Gemini and FastAPI.

---

## 🚀 Overview

Smart Resume Screener is an AI-powered recruitment tool designed to help recruiters screen candidates against job requirements.

The application uses Google Gemini to extract structured information from resumes and semantically compare candidates with a given job description.

### Key Capabilities

- Upload PDF/TXT resumes
- Extract candidate information using Gemini
- Extract skills, education, experience, projects, and certifications
- Enter a job title and job description
- Perform semantic candidate-to-job matching
- Generate a match score from 1–10
- Identify candidate strengths
- Identify skill gaps
- Generate an AI-powered justification
- Store candidates and matching results
- Rank candidates based on match score

---

## 🎥 Demo Video

**Coming soon**

> A 2–3 minute walkthrough demonstrating resume parsing, AI matching, scoring, and candidate ranking will be added here.

---

# ✨ Features

## 1. AI Resume Parsing

The recruiter can upload a PDF or TXT resume.

Gemini extracts structured information including:

- Candidate name
- Email
- Phone number
- Skills
- Education
- Experience
- Projects
- Certifications

The extracted information is displayed in the Parsed Candidate section.

## 2. Job Description Input

The recruiter can provide:

- Job title
- Complete job description

The job description is used as the basis for candidate matching.

## 3. Semantic Candidate Matching

The system uses Gemini to compare the candidate's resume with the job description.

The matching process considers:

- Technical skills
- Relevant experience
- Education
- Projects
- Certifications
- Required qualifications
- Preferred qualifications
- Skill gaps

The system is designed to evaluate semantic relevance rather than relying only on exact keyword matching.

## 4. AI Match Analysis

The system generates:

- Match score out of 10
- Strengths
- Skill gaps
- AI-generated justification

## 5. Candidate Ranking

Matching results are stored and displayed in descending order of match score.

This allows recruiters to quickly identify the most relevant candidates.

---

# 🏗️ System Architecture

```text
                     ┌─────────────────────┐
                     │      Frontend       │
                     │   HTML / CSS / JS   │
                     └──────────┬──────────┘
                                │
                                │ HTTP / REST
                                ▼
                     ┌─────────────────────┐
                     │       FastAPI       │
                     │      Backend        │
                     └──────────┬──────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
       ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
       │ PDF Parser  │   │  Gemini AI  │   │  Database   │
       │             │   │             │   │   SQLite    │
       └──────┬──────┘   └──────┬──────┘   └─────────────┘
              │                 │
              └──────────┬──────┘
                         ▼
                Structured Candidate
                         +
                   Match Analysis
```

## Processing Flow

```text
Resume Upload
      ↓
Resume Text Extraction
      ↓
Gemini Resume Parsing
      ↓
Structured Candidate Data
      ↓
Candidate Stored in Database
      ↓
Job Description Input
      ↓
Gemini Semantic Matching
      ↓
Match Score + Strengths + Skill Gaps + Justification
      ↓
Match Stored in Database
      ↓
Candidate Ranking
```

---

# 🧠 LLM Integration

Google Gemini is the core AI component of the Smart Resume Screener.

The LLM is used for two main tasks:

## 1. Resume Information Extraction

The uploaded resume is first converted into text. The extracted text is then provided to Gemini to identify and structure candidate information.

The model extracts:

- Candidate name
- Email
- Phone number
- Skills
- Education
- Experience
- Projects
- Certifications

The extracted information is returned in a structured format and stored in the application database.

### Resume Extraction Prompt

```text
You are an AI resume parsing assistant.

Analyze the provided resume text and extract structured candidate information.

Extract:
1. Candidate name
2. Email
3. Phone number
4. Skills
5. Education
6. Experience
7. Projects
8. Certifications

Return the information as structured JSON.

Only extract information that is present in the resume.
Do not invent or assume candidate information.
```

---

## 2. Semantic Candidate Matching

After the resume is parsed, the candidate profile is compared with the provided job description using Google Gemini.

The model evaluates the candidate based on:

- Technical skills
- Relevant experience
- Education
- Projects
- Certifications
- Required qualifications
- Preferred qualifications
- Missing or weak requirements

The model generates:

- Match score from 1–10
- Candidate strengths
- Skill gaps
- AI-generated justification

### Candidate Matching Prompt

```text
You are an AI recruitment assistant.

Compare the candidate's resume against the provided job description.

Evaluate the candidate based on:

1. Technical skills
2. Relevant experience
3. Education
4. Projects
5. Certifications
6. Required qualifications
7. Preferred qualifications
8. Missing or weak requirements

Generate:

- Match score from 1 to 10
- Key strengths
- Skill gaps
- Concise justification

Return the result as structured JSON.

Base the evaluation only on the information available in the candidate's resume and the provided job description.

Do not invent candidate experience, skills, qualifications, or achievements.
```

---

## 🔄 LLM Processing Flow

```text
Resume Text
     ↓
Gemini Resume Extraction
     ↓
Structured Candidate Profile
     ↓
Candidate + Job Description
     ↓
Gemini Semantic Matching
     ↓
Match Score
     +
Strengths
     +
Skill Gaps
     +
AI Justification
```

### Why Gemini?

Gemini enables the system to understand the context and meaning of candidate experience and job requirements, allowing the screener to identify relevant qualifications even when the resume and job description use different terminology.

---

# 🛠️ Technology Stack

## Frontend

- HTML
- CSS
- JavaScript

## Backend

- Python
- FastAPI
- SQLAlchemy

## AI

- Google Gemini
- `google-genai`

## Database

- SQLite
- SQLAlchemy ORM

## Document Processing

- PDF text extraction
- TXT file processing

---

# 📁 Project Structure

```text
smart-resume-screener/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   │
│   ├── services/
│   │   ├── pdf_parser.py
│   │   ├── resume_parser.py
│   │   └── matcher.py
│   │
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
│
├── api/
│   └── index.py
│
├── run.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── vercel.json
```

---

# 🔌 API Endpoints

## Health Check

```text
GET /api/health
```

Checks whether the backend is running and whether Gemini is configured.

## Upload Resume

```text
POST /api/resumes/upload
```

Uploads and parses a candidate resume.

## Create Match

```text
POST /api/match
```

Matches a candidate against a job description.

## Get Candidates

```text
GET /api/candidates
```

Returns stored candidates.

## Get Candidate

```text
GET /api/candidates/{candidate_id}
```

Returns information about a specific candidate.

## Get Matches

```text
GET /api/matches
```

Returns candidate matching results ordered by score.

## Interactive API Documentation

FastAPI provides interactive API documentation at:

```text
/docs
```

---

# ⚙️ Local Setup

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd smart-resume-screener
```

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

## 3. Activate the Environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure Gemini

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Never commit the `.env` file to GitHub.

## 6. Run the Application

```bash
python run.py
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

# 🔐 Environment Variables

The application uses:

```env
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
```

API keys should be stored as environment variables and must not be committed to the repository.

For deployment, configure environment variables through the hosting platform.

---

# 📊 Example Workflow

### Step 1 — Upload Resume

The recruiter uploads a candidate resume.

### Step 2 — Parse Resume

Gemini extracts structured candidate information.

### Step 3 — Review Candidate

The recruiter can view:

- Skills
- Education
- Experience
- Projects
- Certifications

### Step 4 — Enter Job Description

The recruiter enters the target job title and requirements.

### Step 5 — Analyze Match

Gemini compares the candidate against the job description.

### Step 6 — Review AI Result

The system displays:

```text
Match Score
Strengths
Skill Gaps
AI Justification
```

### Step 7 — Candidate Ranking

Candidates are ranked according to their generated match scores.

---

# 🔒 Security

- Gemini API keys are stored in environment variables.
- `.env` must not be committed.
- Candidate resumes should not be committed to the repository.
- `.venv` and Python cache files should not be committed.
- API credentials should only be configured through environment variables.

---

# 🚧 Future Improvements

Possible improvements include:

- Batch resume processing
- Recruiter authentication
- Candidate comparison
- Advanced candidate filtering
- Multiple job-description matching
- Persistent cloud database
- Recruiter analytics dashboard
- Candidate search
- Bias and fairness evaluation
- Production-scale deployment

---

# 🎥 Demo

The 2–3 minute demonstration will show:

1. Resume upload
2. AI resume parsing
3. Skills, education, experience, projects, and certifications
4. Job description input
5. AI semantic matching
6. Match score
7. Strengths and skill gaps
8. AI justification
9. Candidate ranking

**Demo Video:** Coming soon

---

# 👨‍💻 Project

## Smart Resume Screener

An AI-powered recruitment screening application built with:

- FastAPI
- Google Gemini
- SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript
