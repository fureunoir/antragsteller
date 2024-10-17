from pydantic import BaseModel, Field
from typing import Optional

class UserModel(BaseModel):
    telegram_id: int = Field(..., description="Unique Telegram ID")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    is_admin: bool = Field(False, description="Is the user an admin")
    is_active: bool = Field(True, description="Is the user active (not banned)")

    class Config:
        schema_extra = {
            "example": {
                "telegram_id": 123456789,
                "first_name": "John",
                "last_name": "Doe",
                "is_admin": False,
                "is_active": True
            }
        }
