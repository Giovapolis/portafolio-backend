from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, blogs, courses, cv, experience, profile, projects, skills, education

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth routes (both /auth/* and /users/*)
app.include_router(auth.router_auth)
app.include_router(auth.router_users)

# Profile routes (both /profile/* and /profiles/*)
app.include_router(profile.router_singular)
app.include_router(profile.router_plural)

# Other routes
app.include_router(experience.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(courses.router)
app.include_router(education.router)
app.include_router(blogs.router)
app.include_router(cv.router)