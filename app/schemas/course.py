from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    platform: str
    certificate_url: str | None = None
    date: str | None = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True