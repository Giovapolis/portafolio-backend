from typing import Optional
from pydantic import BaseModel

class SkillBase(BaseModel):
    name: str
    level: int = 0
    category: str
    order: int = 0


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    category: Optional[str] = None
    order: Optional[int] = None


class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True
