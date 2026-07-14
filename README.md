# portafolio-backend

API REST de portafolio CV. FastAPI + PostgreSQL + JWT.

## Stack

- **Framework:** FastAPI 0.128 (Python 3.12)
- **ORM:** SQLAlchemy 2.0
- **DB:** PostgreSQL 16
- **Auth:** JWT (python-jose) + bcrypt con pre-hash SHA-256
- **PDF:** WeasyPrint + Jinja2
- **Migrations:** Alembic
- **Tests:** pytest + TestClient

## Endpoints

| Método | Path | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/health` | No | Health check + DB status |
| POST | `/auth/login` | No | Login (form-data), devuelve JWT |
| GET | `/auth/me` | JWT | Info del admin autenticado |
| GET | `/profile/` | No | Perfil público |
| PUT | `/profile/` | JWT | Actualizar perfil |
| GET | `/experience/` | No | Listar experiencias |
| POST | `/experience/` | JWT | Crear experiencia |
| PUT | `/experience/{id}` | JWT | Actualizar experiencia |
| DELETE | `/experience/{id}` | JWT | Eliminar experiencia |
| GET | `/education/` | No | Listar educación |
| POST | `/education/` | JWT | Crear educación |
| PUT | `/education/{id}` | JWT | Actualizar educación |
| DELETE | `/education/{id}` | JWT | Eliminar educación |
| GET | `/skills/` | No | Listar skills |
| POST | `/skills/` | JWT | Crear skill |
| PUT | `/skills/{id}` | JWT | Actualizar skill |
| DELETE | `/skills/{id}` | JWT | Eliminar skill |
| GET | `/projects/` | No | Listar proyectos |
| GET | `/projects/{id}` | No | Detalle de proyecto |
| POST | `/projects/` | JWT | Crear proyecto |
| PUT | `/projects/{id}` | JWT | Actualizar proyecto |
| DELETE | `/projects/{id}` | JWT | Eliminar proyecto |
| GET | `/courses/` | No | Listar cursos |
| POST | `/courses/` | JWT | Crear curso |
| PUT | `/courses/{id}` | JWT | Actualizar curso |
| DELETE | `/courses/{id}` | JWT | Eliminar curso |
| GET | `/blog/` | No | Listar posts publicados |
| GET | `/blog/{slug}` | No | Detalle de post por slug |
| POST | `/blog/` | JWT | Crear post |
| PUT | `/blog/{id}` | JWT | Actualizar post |
| DELETE | `/blog/{id}` | JWT | Eliminar post |
| GET | `/cv/pdf` | No | Descargar CV en PDF |

## Desarrollo local

```bash
cp .env.example .env
# Editar .env con credenciales de PostgreSQL

uvicorn app.main:app --reload
# http://localhost:8000

# Seed admin + tablas
python -m app.db.init_db
# Admin por defecto: Giovapolis / GioAdmin2026
```

### Tests

```bash
pytest -v
```

Requiere PostgreSQL con DB `test_portafolio` (configurable via `TEST_DATABASE_URL`).

## Docker

```bash
docker compose up --build
```

Construye imagen y expone en `localhost:8000`. Requiere `.env` con `DATABASE_URL` apuntando a un host PostgreSQL (no incluido en el compose).

## Producción

La imagen se despliega en `ghcr.io/giovapolis/portafolio-backend:latest`.

Pasos:

1. Build & push a GHCR (GitHub Actions o manual)
2. En el servidor: `docker compose pull && docker compose up -d`

El servidor usa Traefik como reverse proxy y PostgreSQL externo. Ver `giovapolis-server/compose/portafolio.yml` para la configuración completa de producción.

## Estructura

```
app/
├── main.py              # FastAPI app + routers
├── api/routes/          # Endpoints por recurso
├── core/                # Config, security, deps
├── db/                  # Session, init_db
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── services/            # PDF generation
└── templates/           # Jinja2 template para CV
tests/                   # pytest
alembic/                 # Migrations
```
