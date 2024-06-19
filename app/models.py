from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel, EmailStr, Field, SecretStr, validator
from typing import List, Dict, Optional

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,  autoincrement=True)
    username = Column(String(25), unique=True,index=True)
    first_name = Column(String(50), unique=False,index=True)
    last_name = Column(String(50), unique=False,index=True)
    email = Column(String(100), unique=True)
    password = Column(String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }


class CreateUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    message : str
    user    : dict

class UserListResponse(BaseModel):
    message: str
    page: int
    users: List[dict]
    next_page_token: Optional[str]


class TokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str

class UserAuthorizedResponse(BaseModel):
    message: str
    user: dict

class UserUpdate(BaseModel):
    user_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
