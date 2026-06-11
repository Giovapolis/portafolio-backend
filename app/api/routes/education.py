from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.education import Education
from app.models.profile import Profile
from app.models.user import User
from app.schemas.education import EducationCreate, EducationResponse, EducationUpdate
from app.core.deps import get_current_admin

router = APIRouter(prefix="/education", tags=["Education"])


@router.get("/", response_model=list[EducationResponse])
def list_education(
    profile_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Education)
    if profile_id is not None:
        query = query.filter(Education.profile_id == profile_id)
    return query.all()


@router.post("/", response_model=EducationResponse)
def create_education(
    data: EducationCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    profile = db.query(Profile).filter(Profile.id == data.profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    if profile.user_id != admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot add education to this profile",
        )

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
    admin: User = Depends(get_current_admin),
):
    education = db.get(Education, education_id)
    if not education:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")

    profile = db.get(Profile, education.profile_id)
    if not profile or profile.user_id != admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify this education entry",
        )

    for key, value in data.model_dump().items():
        setattr(education, key, value)

    db.commit()
    db.refresh(education)
    return education


@router.delete("/{education_id}")
def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    education = db.get(Education, education_id)
    if not education:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")

    profile = db.get(Profile, education.profile_id)
    if not profile or profile.user_id != admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete this education entry",
        )

    db.delete(education)
    db.commit()
    return {"ok": True}
