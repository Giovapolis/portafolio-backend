from typing import Optional
from pydantic import BaseModel

class ExperienceBase(BaseModel):
    company: str
    role: str
    description: str
    start_date: str
    end_date: Optional[str] = None
    order: int = 0

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    order: Optional[int] = None

class ExperienceResponse(ExperienceBase):
    id: int

    class Config:
        from_attributes = True