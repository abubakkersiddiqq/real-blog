from typing import Annotated

from fastapi import APIRouter, Depends,status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud, schema, models

router = APIRouter(prefix="/api", tags=["posts"])

#api  posts
@router.get("/posts", response_model= list[schema.PostResponse])
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    posts = await crud.all_post(db)
    return posts

#api create post
@router.post("/posts", response_model= schema.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: schema.PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await crud.get_user(db, user_id=post.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    new_post = models.Post(
        title = post.title,
        content = post.content,
        user_id = post.user_id
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names= ["author"])
    return new_post

#api get specific post
@router.get("/posts/{post_id}", response_model=schema.PostResponse)
async def get_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.get_post(db, post_id= post_id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")

#api PUT - update post
@router.put("/posts/{post_id}", response_model= schema.PostResponse, status_code= status.HTTP_202_ACCEPTED)
async def full_update_post(post_id: int, post_data: schema.PostCreate,  db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.get_post(db, post_id= post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")
    if post_data.user_id != post.user_id:
        user = await crud.get_user(db, user_id= post_data.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
        
    post.title = post_data.title
    post.content = post_data.content
    post.user_id = post_data.user_id
    await db.commit()
    await db.refresh(post, attribute_names= ["author"])
    return post

#api PATCH - update post
@router.patch("/posts/{post_id}", response_model= schema.PostResponse, status_code= status.HTTP_202_ACCEPTED)
async def partial_update_post(post_id: int, post_data: schema.PostUpdate,  db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.get_post(db, post_id= post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")

    update_post = post_data.model_dump(exclude_unset= True)
    for field, value in update_post.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post, attribute_names= ["author"])
    return post

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await crud.get_post(db, post_id= post_id)
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")
    
    await db.delete(post)
    await db.commit()