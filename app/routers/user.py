from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, models
from app.database import get_db
from app.routers import token
from fastapi.responses import JSONResponse
from jose import JWTError, jwt

router = APIRouter()

@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=models.UserResponse)
async def create_user(user: models.CreateUserRequest, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    created_user = crud.create_user(db=db, **user.dict())
    return JSONResponse(content={"message": "User created successfully", "user": created_user.to_dict()})

@router.get("/users/{username}", status_code=status.HTTP_200_OK, response_model= models.UserResponse)
async def read_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return JSONResponse(content={"message": "User found", "user": user.to_dict()})
'''
@router.get("/users", status_code=status.HTTP_200_OK, response_model=models.UserListResponse)
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=404, detail="No users Found")
    return JSONResponse(content={"message": "Users retrieved successfully", "users": [user.to_dict() for user in users]})'''

@router.get("/users", status_code=status.HTTP_200_OK, response_model=models.UserListResponse)
async def get_users(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1), db: Session = Depends(get_db)):
    total_users = crud.get_total_users_count(db)
    if total_users == 0:
        return models.UserListResponse(message="No users found")

    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_users)
    
    users = crud.get_users(db=db, skip=start_index, limit=per_page)
    
    next_page_token = None
    if end_index < total_users:
        next_users = crud.get_users(db=db, skip=end_index, limit=per_page)
        next_page_data = {
            "page": page + 1,
            "per_page": per_page,
            "next_users": [user.to_dict() for user in next_users]
        }
        next_page_token = jwt.encode(next_page_data, "secret", algorithm="HS256")
        
    return models.UserListResponse(
        message="Users retrieved successfully",
        page=page,
        users=[user.to_dict() for user in users],
        next_page_token=next_page_token
    )

@router.put("/users/{username}", status_code=status.HTTP_200_OK, response_model=models.UserResponse)
async def update_user(username: str, user_update: models.UserUpdate, db: Session = Depends(get_db)):
    update_data = user_update.dict(exclude_unset=True)
    updated_user = crud.update_user(db=db, username=username, user_update=user_update, **update_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return {"message": "User updated successfully", "user": updated_user.to_dict()}


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=models.UserResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    return JSONResponse(content={"message": "User deleted successfully", "user": user.to_dict()})
