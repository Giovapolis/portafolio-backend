from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import ProfileOut, ProfileUpdate
from app.core.deps import get_current_admin

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=ProfileOut)
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile


@router.put("/", response_model=ProfileOut)
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    profile = db.query(Profile).first()
    if not profile:
        profile = Profile(**data.model_dump(exclude_none=True))
        db.add(profile)
    else:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile