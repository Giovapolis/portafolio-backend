from pydantic import BaseModel


class EducationBase(BaseModel):
    profile_id: int
    institution: str
    degree: str
    description: str
    year: str


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    institution: str
    degree: str
    description: str
    year: str


class EducationResponse(EducationUpdate):
    id: int
    profile_id: int

    class Config:
        from_attributes = True
