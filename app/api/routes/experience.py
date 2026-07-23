from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.experience import Experience
from app.schemas.experience import (
    ExperienceCreate,
    ExperienceUpdate,
    ExperienceResponse,
)

from app.core.deps import get_current_admin

router = APIRouter(prefix="/experience", tags=["Experience"])

@router.get("/", response_model=list[ExperienceResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(Experience).order_by(Experience.order).all()

@router.post("/", response_model=ExperienceResponse)
def create(data: ExperienceCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    exp = Experience(**data.model_dump())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@router.put("/{exp_id}", response_model=ExperienceResponse)
def update(exp_id: int, data: ExperienceUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    exp = db.get(Experience, exp_id)
    if not exp:
        raise HTTPException(404, "Experience not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(exp, key, value)

    db.commit()
    db.refresh(exp)
    return exp

@router.delete("/{exp_id}")
def delete(exp_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    exp = db.get(Experience, exp_id)
    if not exp:
        raise HTTPException(404, "Experience not found")

    db.delete(exp)
    db.commit()
    return {"ok": True}