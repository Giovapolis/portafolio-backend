from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token, hash_password
from app.core.deps import get_current_admin
from app.schemas.user import UserCreate, UserOut, TokenResponse

# Create dual routers: /auth/* (kept for backward compatibility) and /users/* (primary)
router_auth = APIRouter(prefix="/auth", tags=["Auth"])
router_users = APIRouter(prefix="/users", tags=["Users"])


@router_auth.post("/login", response_model=TokenResponse)
@router_users.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user with username and password"""
    
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token({"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut.model_validate(user)
    }


@router_users.post("/register", response_model=TokenResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(data.password)
    new_user = User(
        username=data.username,
        email=data.email,
        password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create token
    access_token = create_access_token({"sub": new_user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut.model_validate(new_user)
    }


@router_users.get("/me", response_model=UserOut)
def get_current_user(current_user: User = Depends(get_current_admin)):
    """Get current authenticated user"""
    return UserOut.model_validate(current_user)


# Export both routers
router = router_auth
