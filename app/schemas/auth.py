from pydantic import BaseModel

from app.schemas.user import UserOut


class RegisterResponse(BaseModel):
    """Success response returned after registering a user."""

    message: str
    user: UserOut
