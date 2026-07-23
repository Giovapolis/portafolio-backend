from app.db.session import engine, Base, SessionLocal
from app.models.user import User
from app.models.profile import Profile
from app.models.blog import Blog
from app.models.experience import Experience
from app.models.projects import Project
from app.models.skills import Skill
from app.models.courses import Course
from app.models.education import Education
from app.core.security import hash_password

ADMIN_USER = "Giovapolis"
ADMIN_PASS = "GioAdmin2026"
ADMIN_EMAIL = "giovapolis@portfolio.com"


def init():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == ADMIN_USER).first()

        if not user:
            print("Creating admin user...")

            admin = User(
                username=ADMIN_USER,
                email=ADMIN_EMAIL,
                password=hash_password(ADMIN_PASS)
            )

            db.add(admin)
            db.commit()
            db.refresh(admin)

            print(f"Admin user created: {ADMIN_USER}")
            print(f"   Email: {ADMIN_EMAIL}")
            print(f"   Password: {ADMIN_PASS}")
        else:
            print(f"Admin user already exists: {ADMIN_USER}")

        profile = db.query(Profile).first()
        if not profile:
            profile = Profile(
                name="Your Name",
                title="Your Title",
                bio="Your bio goes here",
                email=ADMIN_EMAIL,
                github="https://github.com/yourusername",
                linkedin="https://linkedin.com/in/yourusername",
                location="Your Location"
            )
            db.add(profile)
            db.commit()
            print("Default profile created")

    finally:
        db.close()


if __name__ == "__main__":
    init()