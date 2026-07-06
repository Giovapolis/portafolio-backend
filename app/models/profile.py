from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(150))
    bio: Mapped[str] = mapped_column(Text, default="")
    email: Mapped[Optional[str]] = mapped_column(String(120), default="")
    phone: Mapped[Optional[str]] = mapped_column(String(30), default="")
    website: Mapped[Optional[str]] = mapped_column(String(200), default="")
    github: Mapped[str] = mapped_column(String(200), default="")
    linkedin: Mapped[str] = mapped_column(String(200), default="")
    location: Mapped[str] = mapped_column(String(100), default="")
    photo_url: Mapped[str] = mapped_column(String(300), default="")