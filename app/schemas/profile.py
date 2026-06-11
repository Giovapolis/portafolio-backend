from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: str
    title: str
    bio: str
    github: str
    linkedin: str
    location: str
    photo_url: str


class ProfileCreate(ProfileBase):
    user_id: int


class ProfileUpdate(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
