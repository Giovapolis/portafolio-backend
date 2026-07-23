# portafolio-backend — FastAPI Portfolio API

## Commands
- `uvicorn app.main:app --reload` — Start dev server at `http://localhost:8000`
- `python -m app.db.init_db` — Create tables + seed admin user (`Giovapolis` / `GioAdmin2026`)
- Tests: `pytest` (runs `tests/`)
- Docker: `docker compose up --build`
- CI/CD: Push to `master` → GitHub Actions builds & pushes to `ghcr.io/giovapolis/portafolio-backend:latest`
- Deploy: On server → `sudo bash /srv/repositories/giovapolis-server/scripts/deploy-portafolio.sh`

## Tech Stack
- **Framework**: FastAPI (Python 3.12)
- **ORM**: SQLAlchemy (sessionmaker, `echo=True`)
- **DB**: PostgreSQL (via `DATABASE_URL` env); falls back to SQLite for testing
- **Auth**: JWT (`python-jose`) + SHA256-prehashed bcrypt (`passlib + bcrypt`)
- **Validation**: Pydantic v2 (`model_validate()`, `model_dump()`, `from_attributes = True`)
- **PDF**: WeasyPrint + Jinja2 HTML template
- **Testing**: pytest

## Project Structure
```
app/
  main.py                       # FastAPI app, CORS (allow all origins), router mounts
  api/routes/
    auth.py                     # POST /auth/login, GET /auth/me
    profile.py                  # GET /profile/, PUT /profile/
    experience.py               # CRUD /experience/
    education.py                # CRUD /education/
    skills.py                   # CRUD /skills/
    projects.py                 # CRUD /projects/
    courses.py                  # CRUD /courses/
    blogs.py                    # CRUD /blog/
    cv.py                       # GET /cv/pdf (PDF download)
  core/
    config.py                   # Env loading via python-dotenv (DATABASE_URL, SECRET_KEY, ALGORITHM)
    security.py                 # hash_password, verify_password, create_access_token
    deps.py                     # get_current_admin (JWT Bearer guard)
  db/
    session.py                  # Engine, SessionLocal, Base, get_db
    init_db.py                  # Table creation + admin seeding
  models/                       # SQLAlchemy ORM models
    user.py                     # User (id, username, email, password)
    profile.py                  # Profile (id, name, title, bio, email, phone, website, github, linkedin, location, photo_url)
    experience.py               # Experience (id, company, role, description, start_date, end_date, order)
    education.py                # Education (id, institution, degree, description, year)
    skills.py                   # Skill (id, name, level, category, order)
    projects.py                 # Project (id, title, description, image_url, repo_url, demo_url, featured, order)
    courses.py                  # Course (id, title, platform, certificate_url, date)
    blog.py                     # Blog (id, title, slug, content_md, excerpt, tags[], is_published, created_at, updated_at)
  schemas/                      # Pydantic v2 request/response schemas (mirror models)
    user.py                     # UserOut, TokenResponse
    profile.py                  # ProfileOut, ProfileUpdate
    experience.py               # ExperienceCreate, ExperienceUpdate, ExperienceResponse
    education.py                # EducationCreate, EducationUpdate, EducationResponse
    skill.py                    # SkillCreate, SkillUpdate, SkillOut
    project.py                  # ProjectCreate, ProjectUpdate, ProjectOut
    course.py                   # CourseCreate, CourseUpdate, CourseOut
    blog.py                     # BlogCreate, BlogUpdate, BlogOut
  services/
    pdf_service.py              # generate_cv_pdf(): Jinja2 + WeasyPrint
  templates/
    cv.html                     # Jinja2 template for CV PDF
  repositories/                 # Placeholder (empty — repository pattern intended but not implemented)
tests/                          # pytest tests
  conftest.py                   # Test fixtures (test DB, test client, auth headers)
  test_auth.py                  # Auth endpoint tests
  test_profile.py               # Profile endpoint tests
  test_sections.py              # Section CRUD endpoint tests
```

## Complete API Reference

### Auth
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/login` | No | Login (form-urlencoded), returns `{ access_token, token_type, user }` |
| GET | `/auth/me` | Admin | Current user info |

### Profile (singular + plural routing)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/profile/` | No | Get profile |
| PUT | `/profile/` | Admin | Create or update profile |

### Experience
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/experience/` | No | List all (ordered by `order`) |
| POST | `/experience/` | Admin | Create |
| PUT | `/experience/{id}` | Admin | Update |
| DELETE | `/experience/{id}` | Admin | Delete |

### Education
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/education/` | No | List all |
| POST | `/education/` | Admin | Create |
| PUT | `/education/{id}` | Admin | Update |
| DELETE | `/education/{id}` | Admin | Delete |

### Skills
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/skills/` | No | List all (ordered by category, then order desc) |
| POST | `/skills/` | Admin | Create |
| PUT | `/skills/{id}` | Admin | Update |
| DELETE | `/skills/{id}` | Admin | Delete |

### Projects
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/projects/` | No | List all (ordered by order desc) |
| GET | `/projects/{id}` | No | Get by ID |
| POST | `/projects/` | Admin | Create |
| PUT | `/projects/{id}` | Admin | Update |
| DELETE | `/projects/{id}` | Admin | Delete |

### Courses
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/courses/` | No | List all |
| POST | `/courses/` | Admin | Create |
| PUT | `/courses/{id}` | Admin | Update |
| DELETE | `/courses/{id}` | Admin | Delete |

### Blog
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/blog/` | No | List published posts (ordered by created_at desc) |
| GET | `/blog/{slug}` | No | Get published post by slug |
| POST | `/blog/` | Admin | Create (slug must be unique) |
| PUT | `/blog/{id}` | Admin | Update |
| DELETE | `/blog/{id}` | Admin | Delete |

### CV / PDF
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/cv/pdf` | No | Download CV as PDF |

## Key Quirks & Notes
- **Dual routers**: `auth.py` exports both `router_auth` (`/auth/*`) and `router_users` — but only `router_auth` is mounted. `profile.py` exports `router_singular` (`/profile/*`) and `router_plural` — only `router_singular` is mounted in `main.py`.
- **`cv.py` used to define its own `get_db()`** — now imports `get_db` from `app.db.session` (fixed).
- **No authentication/authorization separation** — `get_current_admin` is both authn + authz; any authenticated user is an admin.
- **Auth guard**: `get_current_admin` in `core/deps.py` extracts Bearer token, decodes JWT with `JWTError` catch (not bare `except:`), looks up user by `sub` (username), and validates `username is not None`.
- **Login endpoint**: performs dummy password verification when username does not exist (timing-attack mitigation) using `_DUMMY_HASH`.
- **Password hashing**: SHA256-prehashed bcrypt (`hashlib.sha256` + `bcrypt.hashpw`). `verify_password` uses only the prehashed path (no fallback to plain-text encode — fixed).
- **CORS**: `allow_origins` explicitly set to `["https://giovapolis.duckdns.org", "http://localhost:3000", "http://localhost:5173"]` with `allow_credentials=True` (avoids wildcard+credentials spec violation). `expose_headers=["Content-Disposition"]` added for PDF download.
- **Global exception handler** in `main.py` catches unhandled exceptions and returns `500 {"detail": "Internal server error"}`.
- **`init_db.py`** now creates default profile even when admin user already exists (not only on first run).
- **Auth dependency naming** standardized to `admin=Depends(get_current_admin)` across all route files.
- **PDF** requires a working GTK/Cairo install on Windows (WeasyPrint dependency).
- **Alembic** is in `requirements.txt` but no migrations directory exists — schema managed via `Base.metadata.create_all()`.
- **Env** via `python-dotenv` in `app/core/config.py` — copy `.env.example` to `.env`.
- **Pydantic v2**: use `model_validate()` not `from_orm()`; `from_attributes = True` not `orm_mode`; use `model_dump()` not `.dict()` for new code.
- **`repositories/` directory exists but is empty** — data access goes directly through route handlers with `db.query(...)`.
