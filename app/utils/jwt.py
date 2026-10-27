from datetime import timedelta, datetime, timezone
from typing import Optional

from jose import jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.models.refresh_token import RefreshToken


def create_access_token(data:dict, expires_in:Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_in:
        expire = datetime.now(timezone.utc) + expires_in
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "token_type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: int, db: Session) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "sub": str(subject),
        "exp": expires_at,
        "token_type": "refresh"
    }
    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    stored_token = RefreshToken(
        token=refresh_token,
        user_id=subject,
        expires_at=expires_at
    )
    db.add(stored_token)
    db.commit()
    return refresh_token


def decode_token(token:str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

def revoke_refresh_token(token: str, db: Session) -> None:
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if db_token:
        db_token.is_revoked = True
        db.commit()
