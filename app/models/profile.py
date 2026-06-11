from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(150))
    bio: Mapped[str] = mapped_column(Text)
    github: Mapped[str] = mapped_column(String(200))
    linkedin: Mapped[str] = mapped_column(String(200))
    location: Mapped[str] = mapped_column(String(100))
    photo_url: Mapped[str] = mapped_column(String(300))