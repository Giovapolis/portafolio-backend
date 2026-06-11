from pydantic import BaseModel

class SkillBase(BaseModel):
    name: str
    level: int = 0
    category: str
    order: int = 0


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SkillBase):
    pass


class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True
