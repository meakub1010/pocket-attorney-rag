import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.security import create_access_token
from app.db.session import SessionLocal, get_db
from app.schemas.user import UserOut, UserCreate, UserLogin
from app.services.user_service import create_user, authenticate_user, get_users

logger = logging.getLogger(__name__)

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # logger.info(f"Registering user {user}")
    print(f"Registering user: \n {user}")
    return create_user(db, user.first_name, user.last_name, user.email, user.password)


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token({"sub": str(db_user.id), "role": "user"})

    print(f"Token: {token}")
    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    print(f"Current user: {current_user}")
    return get_users(db)
