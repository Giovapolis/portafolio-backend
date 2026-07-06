from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.education import Education
from app.schemas.education import EducationCreate, EducationResponse, EducationUpdate
from app.core.deps import get_current_admin

router = APIRouter(prefix="/education", tags=["Education"])


@router.get("/", response_model=list[EducationResponse])
def list_education(db: Session = Depends(get_db)):
    return db.query(Education).all()


@router.post("/", response_model=EducationResponse)
def create_education(
    data: EducationCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    education = Education(**data.model_dump())
    db.add(education)
    db.commit()
    db.refresh(education)
    return education


@router.put("/{education_id}", response_model=EducationResponse)
def update_education(
    education_id: int,
    data: EducationUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    education = db.get(Education, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(education, key, value)

    db.commit()
    db.refresh(education)
    return education


@router.delete("/{education_id}")
def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    education = db.get(Education, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")

    db.delete(education)
    db.commit()
    return {"ok": True}