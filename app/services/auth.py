from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def register_user(db: Session, email: str, password: str) -> User:
    """Create a new user with a hashed password and save it to the database."""
    # Hash the password before storing
    hashed_password = get_password_hash(password)

    user = User(email=email, password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
