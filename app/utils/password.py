from typing import Optional

from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.models.user import User


passwordHash = PasswordHash.recommended()

def hash_password(password):
    return passwordHash.hash(password)

def verify_password(plain_password, hashed_password):
    return passwordHash.verify(plain_password, hashed_password)

def authenticate_user(username, password, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    return user if verify_password(password, user.hashed_password) else None
