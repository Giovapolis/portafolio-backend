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


class ProjectUpdate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int

    class Config:
        from_attributes = True
