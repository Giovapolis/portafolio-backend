from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import auth, blogs, courses, cv, experience, health, profile, projects, skills, education

app = FastAPI(title="CV-WEB API")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://giovapolis.duckdns.org",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(experience.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(courses.router)
app.include_router(education.router)
app.include_router(blogs.router)
app.include_router(cv.router)