from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import  Depends, HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext
from app.models import UserUpdate

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_user(db: Session, username: str, first_name: str, last_name: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_total_users_count(db: Session) -> int:
    return db.query(User).count()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, username: str, **kwargs):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    for field, value in kwargs.items():
        if value is not None:
            # Hash the password before setting it
            if field == "password":
                value = pwd_context.hash(value)
            setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user
