from pydantic import BaseModel

class ExperienceBase(BaseModel):
    company: str
    role: str
    description: str
    start_date: str
    end_date: str
    order: int

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(ExperienceBase):
    pass

class ExperienceResponse(ExperienceBase):
    id: int

    class Config:
        from_attributes = True