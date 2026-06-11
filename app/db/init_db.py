from app.db.session import engine, Base, SessionLocal
from app.models.user import User
from app.models.profile import Profile
from app.models.blog import Blog
from app.core.security import hash_password

ADMIN_USER = "Giovapolis"
ADMIN_PASS = "GioAdmin2026"
ADMIN_EMAIL = "giovapolis@portfolio.com"

def init():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Create admin user if doesn't exist
        user = db.query(User).filter(User.username == ADMIN_USER).first()

        if not user:
            print("👤 Creating admin user...")

            admin = User(
                username=ADMIN_USER,
                email=ADMIN_EMAIL,
                password=hash_password(ADMIN_PASS)
            )

            db.add(admin)
            db.commit()
            db.refresh(admin)

            print(f"✅ Admin user created: {ADMIN_USER}")
            print(f"   Email: {ADMIN_EMAIL}")
            print(f"   Password: {ADMIN_PASS}")
            
            # Create default profile
            profile = Profile(
                user_id=admin.id,
                name="Your Name",
                title="Your Title",
                bio="Your bio goes here",
                github="https://github.com/yourusername",
                linkedin="https://linkedin.com/in/yourusername",
                location="Your Location",
                photo_url=""
            )
            db.add(profile)
            db.commit()
            
            print(f"✅ Default profile created")

        else:
            print(f"⚠️ Admin user already exists: {ADMIN_USER}")

    finally:
        db.close()

if __name__ == "__main__":
    init()