from typing import Optional
from pydantic import BaseModel

class ProjectBase(BaseModel):
    title: str
    description: str
    image_url: str | None = None
    repo_url: str | None = None
    demo_url: str
    featured: bool = False
    order: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    featured: Optional[bool] = None
    order: Optional[int] = None


class ProjectOut(ProjectBase):
    id: int

    class Config:
        from_attributes = True
