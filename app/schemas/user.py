from datetime import datetime

from pydantic import BaseModel, EmailStr, model_validator


class UserCreate(BaseModel):
    """Input schema for creating (registering) a user."""

    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("password and confirm_password must match")
        return self


class UserOut(BaseModel):
    """Output schema returned to the client after registration."""

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
