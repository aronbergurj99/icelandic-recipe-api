from dataclasses import Field
from lib2to3.pytree import Base
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserModel(BaseModel):
    username: EmailStr = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "random@randomemail.com",
            }
        }

class UserLoginModel(BaseModel):
    username: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "random@randomemail.com",
                "password": "strongpassword!1234"
            }
        }

class UserDbModel(UserModel):
    role: Optional[str] = 'user'
    hashed_password: str