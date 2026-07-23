from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.projects import Project
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.core.deps import get_current_admin

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=list[ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.order.desc()).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).get(project_id)

    if not project:
        raise HTTPException(404, "Project not found")

    return project


@router.post("/", response_model=ProjectOut)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    project = db.query(Project).get(project_id)

    if not project:
        raise HTTPException(404, "Project not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    project = db.query(Project).get(project_id)

    if not project:
        raise HTTPException(404, "Project not found")

    db.delete(project)
    db.commit()

    return {"ok": True}