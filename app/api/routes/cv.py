from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.pdf_service import generate_cv_pdf

from app.models.profile import Profile
from app.models.experience import Experience
from app.models.projects import Project
from app.models.skills import Skill
from app.models.courses import Course
from app.models.education import Education
from app.models.blog import Blog

router = APIRouter(prefix="/cv", tags=["CV"])


@router.get("/pdf")
def download_cv(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    experience = db.query(Experience).order_by(Experience.order).all()
    education = db.query(Education).all()
    projects = db.query(Project).order_by(Project.order.desc()).all()
    skills = db.query(Skill).order_by(Skill.category, Skill.order.desc()).all()
    courses = db.query(Course).all()
    blog = db.query(Blog).filter(Blog.is_published.is_(True)).order_by(Blog.created_at.desc()).limit(10).all()

    skills_by_category = {}
    for s in skills:
        skills_by_category.setdefault(s.category, []).append(s)

    data = {
        "profile": profile,
        "experience": experience,
        "education": education,
        "projects": projects,
        "skills": skills,
        "skills_by_category": skills_by_category,
        "courses": courses,
        "blog": blog,
    }

    pdf_bytes = generate_cv_pdf(data)

    return Response(
        pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=cv.pdf"}
    )