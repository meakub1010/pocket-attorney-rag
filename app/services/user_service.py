from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password


def create_user(
        db: Session,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        tier: str = "free",
        is_active: bool = True,
        is_verified: bool = False
):
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hash_password(password),
        tier=tier,
        is_active=is_active,
        is_verified=is_verified
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session):
    return db.query(User).all()


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
