from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import ProfileOut, ProfileUpdate, ProfileCreate
from app.core.deps import get_current_admin

# Create routers for both singular and plural endpoints
router_singular = APIRouter(prefix="/profile", tags=["Profile"])
router_plural = APIRouter(prefix="/profiles", tags=["Profile"])

# Shared get_db function
def get_db_session():
    db = get_db().__next__()
    try:
        yield db
    finally:
        db.close()


# ===== PUBLIC ENDPOINTS - GET =====

# GET /profile/ - Get first/default profile (for backward compatibility)
@router_singular.get("/", response_model=ProfileOut)
def get_default_profile(db: Session = Depends(get_db)):
    """Get the default/first profile"""
    profile = db.query(Profile).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


# GET /profiles/ - List all profiles
@router_plural.get("/", response_model=list[ProfileOut])
def list_profiles(db: Session = Depends(get_db)):
    """List all profiles"""
    return db.query(Profile).all()


# GET /profiles/{profile_id} - Get specific profile
@router_plural.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """Get profile by ID"""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


# GET /profiles/user/{user_id} - Get all profiles for a user
@router_plural.get("/user/{user_id}", response_model=list[ProfileOut])
def get_user_profiles(user_id: int, db: Session = Depends(get_db)):
    """Get all profiles for a specific user"""
    profiles = db.query(Profile).filter(Profile.user_id == user_id).all()
    return profiles


# GET /profiles/me - Get current user's profiles
@router_plural.get("/me", response_model=list[ProfileOut])
def get_my_profiles(current_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Get all profiles for current user"""
    profiles = db.query(Profile).filter(Profile.user_id == current_user.id).all()
    return profiles


# ===== ADMIN ENDPOINTS - CREATE, UPDATE, DELETE =====

# PUT /profile/ - Update first/default profile
@router_singular.put("/", response_model=ProfileOut)
def update_default_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Update the default/first profile"""
    profile = db.query(Profile).first()
    
    if not profile:
        # Create new profile if doesn't exist
        profile = Profile(user_id=admin.id, **data.dict())
        db.add(profile)
    else:
        for key, value in data.dict().items():
            setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    
    return profile


# POST /profiles/ - Create new profile
@router_plural.post("/", response_model=ProfileOut)
def create_profile(
    data: ProfileCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Create a new profile"""
    
    # If user_id is not provided, use current user
    user_id = data.user_id if data.user_id else admin.id
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify current user can only create their own profiles
    if user_id != admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create profiles for other users"
        )
    
    profile = Profile(**data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    return profile


# PUT /profiles/{profile_id} - Update specific profile
@router_plural.put("/{profile_id}", response_model=ProfileOut)
def update_profile(
    profile_id: int,
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Update a profile"""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Verify user owns this profile
    if profile.user_id != admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other user's profiles"
        )
    
    for key, value in data.dict().items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    
    return profile


# DELETE /profiles/{profile_id} - Delete profile
@router_plural.delete("/{profile_id}")
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Delete a profile"""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Verify user owns this profile
    if profile.user_id != admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other user's profiles"
        )
    
    db.delete(profile)
    db.commit()
    
    return {"ok": True}


# Export primary router (plural)
router = router_plural
