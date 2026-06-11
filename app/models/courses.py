from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    platform: Mapped[str] = mapped_column(String(100))
    certificate_url: Mapped[str] = mapped_column(String(300))
    date: Mapped[str] = mapped_column(String(50))