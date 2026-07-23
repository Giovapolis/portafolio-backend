from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate, BlogOut
from app.core.deps import get_current_admin

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get("/", response_model=list[BlogOut])
def get_posts(db: Session = Depends(get_db)):
    return (
        db.query(Blog)
        .filter(Blog.is_published == True)
        .order_by(Blog.created_at.desc())
        .all()
    )


@router.get("/{slug}", response_model=BlogOut)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(Blog).filter(Blog.slug == slug).first()

    if not post or not post.is_published:
        raise HTTPException(404, "Post not found")

    return post


@router.post("/", response_model=BlogOut)
def create_post(
    data: BlogCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    existing = db.query(Blog).filter(Blog.slug == data.slug).first()
    if existing:
        raise HTTPException(400, "Slug already exists")

    post = Blog(**data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=BlogOut)
def update_post(
    post_id: int,
    data: BlogUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    post = db.query(Blog).get(post_id)

    if not post:
        raise HTTPException(404, "Post not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    post = db.query(Blog).get(post_id)

    if not post:
        raise HTTPException(404, "Post not found")

    db.delete(post)
    db.commit()

    return {"ok": True}