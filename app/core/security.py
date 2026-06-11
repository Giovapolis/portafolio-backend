import hashlib
import bcrypt
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY, ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60
_BCRYPT_ROUNDS = 12

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def _sha256_hexdigest_bytes(password: str) -> bytes:
    return hashlib.sha256(password.encode()).hexdigest().encode()

def hash_password(password: str):
    prehashed = _sha256_hexdigest_bytes(password)
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(prehashed, salt)

    return hashed.decode()

def verify_password(plain, hashed):
    hp_bytes = hashed.encode()

    prehashed = _sha256_hexdigest_bytes(plain)
    if bcrypt.checkpw(prehashed, hp_bytes):
        return True
    
    try:
        return bcrypt.checkpw(plain.encode(), hp_bytes)
    except ValueError:
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
