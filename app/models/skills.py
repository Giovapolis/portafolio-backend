from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    level: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(100))
    order: Mapped[int] = mapped_column(Integer)