import json
import os
import shutil
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

load_dotenv()

from .database import Base, engine, get_db
from .models import Candidate, JobDescription, Match
from .services.pdf_parser import extract_text_from_pdf
from .services.resume_parser import parse_resume


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Resume Screener",
    version="1.0.0",
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "ai_provider": "Gemini",
        "ai_enabled": bool(os.getenv("GEMINI_API_KEY")),
        "model": os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        ),
    }


def extract_resume_text(path: Path, extension: str) -> str:
    if extension == ".pdf":
        return extract_text_from_pdf(str(path))

    if extension == ".txt":
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    raise ValueError(
        "Unsupported resume format."
    )


@app.post("/api/resumes/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    original_name = Path(file.filename).name
    extension = Path(original_name).suffix.lower()

    if extension not in {".pdf", ".txt"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT resumes are supported.",
        )

    safe_name = (
        f"{uuid.uuid4().hex}_{original_name}"
    )

    path = UPLOAD_DIR / safe_name

    with path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    try:
        # 1. Extract raw resume text
        text = extract_resume_text(
            path,
            extension,
        )

        if not text.strip():
            raise ValueError(
                "No readable text was found in the resume."
            )

        # 2. Extract structured information with Gemini
        data = parse_resume(text)

        # 3. Store candidate
        candidate = Candidate(
            name=data.get(
                "name",
                "Unknown Candidate",
            ),
            email=data.get(
                "email",
                "",
            ),
            phone=data.get(
                "phone",
                "",
            ),
            resume_filename=original_name,
            resume_text=text,
            skills=json.dumps(
                data.get("skills", [])
            ),
            education=json.dumps(
                data.get("education", [])
            ),
            experience=json.dumps(
                data.get("experience", [])
            ),
            projects=json.dumps(
                data.get("projects", [])
            ),
            certifications=json.dumps(
                data.get("certifications", [])
            ),
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return {
            "candidate_id": candidate.id,
            "candidate": serialize_candidate(
                candidate
            ),
        }

    except Exception as exc:
        db.rollback()

        if path.exists():
            path.unlink()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@app.post("/api/match")
def create_match(
    candidate_id: int = Form(...),
    job_title: str = Form("Untitled Job"),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
):
    candidate = db.get(
        Candidate,
        candidate_id,
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found.",
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description is required.",
        )

    from .services.matcher import match_candidate

    # -------------------------------------------------
    # Check whether this exact candidate/job already
    # has a match.
    # -------------------------------------------------

    existing_job = (
        db.query(JobDescription)
        .filter(
            JobDescription.title == job_title,
            JobDescription.description == job_description,
        )
        .first()
    )

    if existing_job:

        existing_match = (
            db.query(Match)
            .filter(
                Match.candidate_id == candidate.id,
                Match.job_id == existing_job.id,
            )
            .first()
        )

        if existing_match:
            result = match_candidate(
                candidate.resume_text,
                job_description,
            )

            existing_match.score = float(
                result.get(
                    "match_score",
                    0,
                )
            )

            existing_match.strengths = json.dumps(
                result.get(
                    "strengths",
                    [],
                )
            )

            existing_match.skill_gaps = json.dumps(
                result.get(
                    "skill_gaps",
                    [],
                )
            )

            existing_match.justification = result.get(
                "justification",
                "",
            )

            db.commit()
            db.refresh(existing_match)

            return serialize_match(
                existing_match,
                candidate,
                existing_job,
            )

    # -------------------------------------------------
    # New job / new candidate-job combination
    # -------------------------------------------------

    result = match_candidate(
        candidate.resume_text,
        job_description,
    )

    if existing_job:
        job = existing_job
    else:
        job = JobDescription(
            title=job_title,
            description=job_description,
        )

        db.add(job)
        db.flush()

    match = Match(
        candidate_id=candidate.id,
        job_id=job.id,
        score=float(
            result.get(
                "match_score",
                0,
            )
        ),
        strengths=json.dumps(
            result.get(
                "strengths",
                [],
            )
        ),
        skill_gaps=json.dumps(
            result.get(
                "skill_gaps",
                [],
            )
        ),
        justification=result.get(
            "justification",
            "",
        ),
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return serialize_match(
        match,
        candidate,
        job,
    )


@app.get("/api/candidates")
def list_candidates(
    db: Session = Depends(get_db),
):
    candidates = (
        db.query(Candidate)
        .order_by(
            Candidate.created_at.desc()
        )
        .all()
    )

    return [
        serialize_candidate(candidate)
        for candidate in candidates
    ]


@app.get("/api/candidates/{candidate_id}")
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    candidate = db.get(
        Candidate,
        candidate_id,
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found.",
        )

    return serialize_candidate(
        candidate
    )


@app.get("/api/matches")
def list_matches(
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Match)
        .order_by(
            Match.score.desc()
        )
        .all()
    )

    output = []

    for match in rows:

        candidate = db.get(
            Candidate,
            match.candidate_id,
        )

        job = db.get(
            JobDescription,
            match.job_id,
        )

        if candidate and job:
            output.append(
                serialize_match(
                    match,
                    candidate,
                    job,
                )
            )

    return output


def parse_json(value):
    try:
        return json.loads(
            value or "[]"
        )
    except Exception:
        return []


def serialize_candidate(candidate):
    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "phone": candidate.phone,
        "resume_filename":
            candidate.resume_filename,
        "skills":
            parse_json(candidate.skills),
        "education":
            parse_json(candidate.education),
        "experience":
            parse_json(candidate.experience),
        "projects":
            parse_json(candidate.projects),
        "certifications":
            parse_json(candidate.certifications),
        "created_at": (
            str(candidate.created_at)
            if candidate.created_at
            else None
        ),
    }


def serialize_match(
    match,
    candidate,
    job,
):
    return {
        "id": match.id,
        "candidate_id":
            match.candidate_id,
        "candidate_name":
            candidate.name,
        "job_id":
            job.id,
        "job_title":
            job.title,
        "score":
            match.score,
        "strengths":
            parse_json(
                match.strengths
            ),
        "skill_gaps":
            parse_json(
                match.skill_gaps
            ),
        "justification":
            match.justification,
        "created_at": (
            str(match.created_at)
            if match.created_at
            else None
        ),
    }