from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Education(Base):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profile.id"), index=True)
    institution: Mapped[str] = mapped_column(String(200))
    degree: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    year: Mapped[str] = mapped_column(String(50))
