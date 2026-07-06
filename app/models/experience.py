from typing import Optional
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Experience(Base):
    __tablename__ = "experience"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)
    start_date: Mapped[str] = mapped_column(String(50))
    end_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    order: Mapped[int] = mapped_column(Integer)