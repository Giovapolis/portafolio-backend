from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.courses import Course
from app.schemas.course import CourseCreate, CourseUpdate, CourseOut
from app.core.deps import get_current_admin

router = APIRouter(prefix="/courses", tags=["Courses"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#PUBLIC
@router.get("/", response_model=list[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

#ADMIN
@router.post("/", response_model=CourseOut)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin)
):
    course = Course(**data.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.put("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    data: CourseUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin)
):
    course = db.query(Course).get(course_id)

    if not course:
        raise HTTPException(404, "Course not found")

    for key, value in data.dict().items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin)
):
    course = db.query(Course).get(course_id)

    if not course:
        raise HTTPException(404, "Course not found")

    db.delete(course)
    db.commit()

    return {"ok": True}