from typing import Optional
from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: str = ""
    title: str = ""
    bio: str = ""
    email: str = ""
    phone: str = ""
    website: str = ""
    github: str = ""
    linkedin: str = ""
    location: str = ""
    photo_url: str = ""


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    location: Optional[str] = None
    photo_url: Optional[str] = None


class ProfileOut(ProfileBase):
    id: int

    class Config:
        from_attributes = True
