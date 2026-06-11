from pydantic import BaseModel
from typing import List, Optional

class BlogBase(BaseModel):
    title: str
    slug: str
    content_md: str
    excerpt: Optional[str] = ""
    tags: List[str] = []
    is_published: bool = True

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int

    class Config:
        from_attributes = True
