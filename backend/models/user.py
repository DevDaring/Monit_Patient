"""User data model."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """User data model."""
    user_id: str
    username: str
    email: EmailStr
    full_name: str
    role: str  # admin, doctor, nurse, technician
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "U001",
                "username": "dr.smith",
                "email": "dr.smith@hospital.com",
                "full_name": "Dr. John Smith",
                "role": "doctor",
                "is_active": True
            }
        }
