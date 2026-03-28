from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends,status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import create_access_token, hash_password, Current_User, verify_password
from config import settings
import crud, schema, models


router = APIRouter(prefix="/api", tags=["users"])

@router.post('/users', response_model= schema.UserPrivate, status_code= status.HTTP_201_CREATED)
async def create_user(user : schema.UserCreate, db : Annotated[AsyncSession, Depends(get_db)]):
    existing_user = await crud.get_user_with_posts(db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Username is already exist"
        )
    existing_email = await crud.get_user_with_posts(db, email=user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Email is already exist"
        )
    new_user = models.User(
        username = user.username,
        email = user.email.lower(),
        password_hash = hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# token
@router.post('/users/token', response_model= schema.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]):
    # Look up user by email (case-insensitive)
    # Note: OAuth2PasswordRequestForm uses "username" field, but we treat it as email

    user = await crud.get_user_for_auth(db, form_data.username.lower())

    # Verify user exists and password is correct
    # Don't reveal which one failed (security best practice)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token with user id as subject
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return schema.Token(access_token=access_token, token_type="bearer")

# user
@router.get("/users/me", response_model=schema.UserPrivate)
async def get_current_user(current_user: Current_User):
    return current_user


#api user 
@router.get('/users/{user_id}', response_model= schema.UserPublic)
async def get_user(user_id : int, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await crud.get_user_with_posts(db, user_id= user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")


@router.get('/users/{user_id}/posts', response_model=list[schema.PostResponse])
async def get_user_posts(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await crud.get_user_with_posts(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.posts 

@router.patch("/users/{user_id}", response_model=schema.UserPrivate)
async def update_user(user_id : int, user_update: schema.UserUpdate, current_user: Current_User, db: Annotated[AsyncSession, Depends(get_db)]):
    
    if user_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not Authorized to update this user")
    
    user = await crud.get_user_with_posts(db, user_id=user_id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    
    if user_update.username is not None and user.username.lower() != user_update.username.lower():  
        existing_user = await crud. get_user_by_username_or_email(db, username= user_update.username)
        if existing_user :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username is already exist")
    
    if user_update.email is not None and user.email.lower() != user_update.email.lower():  
        existing_email = await crud.get_user_by_username_or_email(db, email= user_update.email)
        if existing_email :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is already exist")
        
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.image_file is not None:
        user.image_file = user_update.image_file

    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code =status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: Current_User, db: Annotated[AsyncSession, Depends(get_db)]):
    if user_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not Authorized to delete this User")
    
    user = await crud.get_user_with_posts(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    
    await db.delete(user)
    await db.commit()