from typing import Optional
from pydantic import BaseModel


class EducationBase(BaseModel):
    institution: str = ""
    degree: str = ""
    description: str = ""
    year: str = ""


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    description: Optional[str] = None
    year: Optional[str] = None


class EducationResponse(EducationBase):
    id: int

    class Config:
        from_attributes = True
