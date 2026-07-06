from typing import Optional
from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    platform: str
    certificate_url: str | None = None
    date: str | None = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    platform: Optional[str] = None
    certificate_url: Optional[str] = None
    date: Optional[str] = None

class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True