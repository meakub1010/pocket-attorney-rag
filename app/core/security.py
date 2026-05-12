import uuid
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from jose import JWTError, jwt

from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, tier: str = "free") -> tuple[str, str]:
    jti = str(uuid.uuid4())
    payload = {
        "sub": user_id,
        "type": "access",
        "tier": tier,
        "jti": jti,
        "exp": datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, jti

def create_refresh_token(user_id: str) -> tuple[str, str]:
    jti = str(uuid.uuid4())
    payload = {
        "sub": user_id,
        "jti": jti,
        "type":"refresh",
        "exp": datetime.utcnow() + timedelta(days=3)
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.ALGORITHM)

    return token, jti

def decode_access_token(token: str):
    print(f"token: {token}")
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        print("JWT Error", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")