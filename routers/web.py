from typing import Annotated

from fastapi import APIRouter, Depends,status, HTTPException,Request
from sqlalchemy.orm import Session
from database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
import crud

router = APIRouter(tags=["Frontend"])

templates = Jinja2Templates(directory="templates")


@router.get("/", include_in_schema= False, name='home')
@router.get("/posts", include_in_schema= False, name='posts')
def home(request : Request, db : Annotated[Session, Depends(get_db)]):
    posts = crud.all_post(db)
    return templates.TemplateResponse(
       "home.html",
       {
           "request": request, 
           "posts" : posts,
           "title" : "Home"
       }
    )

#html specifc post
@router.get("/posts/{post_id}", include_in_schema= False)
def post_page(request: Request, post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post(db , post_id=post_id)
    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
            "post.html",
            {
                "request" : request,
                "post" : post,
                "title": title
            }
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

#html user posts
@router.get("/users/{user_id}/posts", include_in_schema= False, name="user_posts")
def user_posts_page(request: Request, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user(db, user_id= user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "user not found")
    posts = crud.get_user_posts(db,user_id= user_id)
    return templates.TemplateResponse(
        "user_posts.html",
        {
            "request" : request,
            "posts" : posts,
            "user" : user,
            "title" : f"{user.username}'s Posts "
        }
    )
