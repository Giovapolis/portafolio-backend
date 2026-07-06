from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.skills import Skill
from app.schemas.skill import SkillCreate, SkillUpdate, SkillOut
from app.core.deps import get_current_admin

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("/", response_model=list[SkillOut])
def get_skills(db: Session = Depends(get_db)):
    return db.query(Skill).order_by(Skill.category, Skill.order.desc()).all()


@router.post("/", response_model=SkillOut)
def create_skill(
    data: SkillCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin)
):
    skill = Skill(**data.model_dump())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.put("/{skill_id}", response_model=SkillOut)
def update_skill(
    skill_id: int,
    data: SkillUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin)
):
    skill = db.query(Skill).get(skill_id)

    if not skill:
        raise HTTPException(404, "Skill not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(skill, key, value)

    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/{skill_id}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin)
):
    skill = db.query(Skill).get(skill_id)

    if not skill:
        raise HTTPException(404, "Skill not found")

    db.delete(skill)
    db.commit()

    return {"ok": True}