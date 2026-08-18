from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import RegisterResponse
from app.schemas.user import UserCreate, UserOut
from app.services.auth import register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create the user (hashes password, saves to DB)
    new_user = register_user(db, payload.email, payload.password)

    return RegisterResponse(
        message="User registered successfully", user=UserOut.model_validate(new_user)
    )
