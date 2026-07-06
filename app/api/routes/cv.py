from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.pdf_service import generate_cv_pdf

from app.models.profile import Profile
from app.models.experience import Experience
from app.models.projects import Project
from app.models.skills import Skill
from app.models.courses import Course

router = APIRouter(prefix="/cv", tags=["CV"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/pdf")
def download_cv(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    experience = db.query(Experience).all()
    projects = db.query(Project).all()
    skills = db.query(Skill).all()
    courses = db.query(Course).all()

    data = {
        "profile": profile,
        "experience": experience,
        "projects": projects,
        "skills": skills,
        "courses": courses,
    }

    pdf_bytes = generate_cv_pdf(data)

    return Response(
        pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=cv.pdf"}
    )