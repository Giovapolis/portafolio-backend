import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import Base, get_db
from app.main import app
from app.core.security import hash_password, create_access_token
from app.models.user import User
from app.models.profile import Profile
from app.models.blog import Blog
from app.models.experience import Experience
from app.models.projects import Project
from app.models.skills import Skill
from app.models.courses import Course
from app.models.education import Education

TEST_DB_URL = os.getenv("TEST_DATABASE_URL", "postgresql://cv_user:giovapolisdb@localhost:5432/test_portafolio")
engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        admin = User(username="Giovapolis", email="giovapolis@portfolio.com", password=hash_password("GioAdmin2026"))
        db.add(admin)
        db.commit()
        profile = Profile(name="Giovapolis", title="Dev", bio="Bio", email="giovapolis@portfolio.com", github="https://github.com/Giovapolis", linkedin="https://linkedin.com/in/Giovapolis", location="Remote")
        db.add(profile)
        db.commit()
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def token():
    return create_access_token({"sub": "Giovapolis"})


@pytest.fixture
def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}
