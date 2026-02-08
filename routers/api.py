from typing import Annotated

from fastapi import APIRouter, Depends,status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud, schema, models

router = APIRouter(prefix="/api", tags=["API"])

@router.post('/users', response_model= schema.UserResponse, status_code= status.HTTP_201_CREATED)
def create_user(user : schema.UserCreate, db : Annotated[Session, Depends(get_db)]):
    existing_user = crud.get_user(db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Username is already exist"
        )
    existing_email = crud.get_user(db, email=user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Email is already exist"
        )
    new_user = models.User(
        username = user.username,
        email = user.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#api user 
@router.get('/users/{user_id}', response_model= schema.UserResponse)
def get_user(user_id : int, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user(db, user_id= user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")

@router.delete("/users/{user_id}", status_code =status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    
    db.delete(user)
    db.commit()

@router.get('/users/{user_id}/posts', response_model=list[schema.PostResponse])
def get_user_posts(user_id : int , db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user(db, user_id = user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    posts = crud.get_user(db, user_id= user_id)
    return posts

@router.patch("/users/{user_id}", response_model=schema.UserResponse)
def update_user(user_id : int, user_update: schema.UserUpdate, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    if user_update.username is not None and user.username != user_update.username:  
        existing_user = crud.get_user(db, user_update.username)
        if existing_user :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username is already exist")
    if user_update.email is not None and user.email != user_update.email:  
        existing_email = crud.get_user(db, user_update.email)
        if existing_email :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is already exist")
        
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.image_file is not None:
        user.image_file = user_update.image_file

    db.commit()
    db.refresh(user)
    return user

#api  posts
@router.get("/posts", response_model= list[schema.PostResponse])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    posts = crud.all_post(db)
    return posts

#api create post
@router.post("/posts", response_model= schema.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: schema.PostCreate, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user(db, user_id=post.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    new_post = models.Post(
        title = post.title,
        content = post.content,
        user_id = post.user_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#api get specific post
@router.get("/posts/{post_id}", response_model=schema.PostResponse)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post(db, post_id= post_id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")

#api PUT - update post
@router.put("/posts/{post_id}", response_model= schema.PostResponse, status_code= status.HTTP_202_ACCEPTED)
def full_update_post(post_id: int, post_data: schema.PostCreate,  db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post(db, post_id= post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")
    if post_data.user_id != post.user_id:
        user = crud.get_user(db, user_id= post_data.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
        
    post.title = post_data.title
    post.content = post_data.content
    post.user_id = post_data.user_id
    db.commit()
    db.refresh(post)
    return post

#api PATCH - update post
@router.patch("/posts/{post_id}", response_model= schema.PostResponse, status_code= status.HTTP_202_ACCEPTED)
def partial_update_post(post_id: int, post_data: schema.PostUpdate,  db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post(db, post_id= post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")

    update_post = post_data.model_dump(exclude_unset= True)
    for field, value in update_post.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post(db, post_id= post_id)
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")
    
    db.delete(post)
    db.commit()