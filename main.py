from typing import Annotated

from fastapi import FastAPI, Request, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse 
from starlette.exceptions import HTTPException as StarletteHTTPException
from schema import PostUpdate, PostCreate, PostResponse, UserResponse, UserCreate, UserUpdate
from sqlalchemy.orm import Session
from database import get_db, engine

import crud
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount('/media', StaticFiles(directory= "media"), name= "media")
 
@app.get("/", include_in_schema= False, name='home')
@app.get("/posts", include_in_schema= False, name='posts')
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
@app.get("/posts/{post_id}", include_in_schema= False)
def post_page(request: Request, post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post_by_post_id(db , post_id=post_id)
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
@app.get("/users/{user_id}/posts", include_in_schema= False, name="user_posts")
def user_posts_page(request: Request, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user_by_user_id(db, user_id= user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "user not found")
    posts = crud.get_user_posts(db, user_id)
    return templates.TemplateResponse(
        "user_posts.html",
        {
            "request" : request,
            "posts" : posts,
            "user" : user,
            "title" : f"{user.username}'s Posts "
        }
    )


#create users
@app.post('/api/users', response_model=UserResponse, status_code= status.HTTP_201_CREATED)
def create_user(user : UserCreate, db : Annotated[Session, Depends(get_db)]):
    existing_user = crud.get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Username is already exist"
        )
    existing_email = crud.get_email_by_username(db, email=user.email)
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
@app.get('/api/users/{user_id}', response_model= UserResponse)
def get_user(user_id : int, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user_by_user_id(db, user_id= user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")

@app.delete("/api/users/{user_id}", status_code =status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user_by_user_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    
    db.delete(user)
    db.commit()

#api user posts
@app.get('/api/users/{user_id}/posts', response_model=list[PostResponse])
def get_user_posts(user_id : int , db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user_by_user_id(db, user_id = user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    posts = crud.get_user_posts(db, user_id= user_id)
    return posts

@app.patch("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id : int, user_update: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user_by_user_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    if user_update.username is not None and user.username != user_update.username:  
        existing_user = crud.get_user_by_username(db, user_update.username)
        if existing_user :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username is already exist")
    if user_update.email is not None and user.email != user_update.email:  
        existing_email = crud.get_email_by_username(db, user_update.email)
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
@app.get("/api/posts", response_model= list[PostResponse])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    posts = crud.all_post(db)
    return posts

#api create post
@app.post("/api/posts", response_model= PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    user = crud.get_user_by_user_id(db, post.user_id)
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
@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post_by_post_id(db, post_id= post_id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")

#api PUT - update post
@app.put("/api/posts/{post_id}", response_model=PostResponse, status_code= status.HTTP_202_ACCEPTED)
def full_update_post(post_id: int, post_data: PostCreate,  db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post_by_post_id(db, post_id= post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")
    if post_data.user_id != post.user_id:
        user = crud.get_user_by_user_id(db, post_data.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
        
    post.title = post_data.title
    post.content = post_data.content
    post.user_id = post_data.user_id
    db.commit()
    db.refresh(post)
    return post

#api PATCH - update post
@app.patch("/api/posts/{post_id}", response_model=PostResponse, status_code= status.HTTP_202_ACCEPTED)
def partial_update_post(post_id: int, post_data: PostUpdate,  db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post_by_post_id(db, post_id= post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")

    update_post = post_data.model_dump(exclude_unset= True)
    for field, value in update_post.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post

@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = crud.get_post_by_post_id(db, post_id= post_id)
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")
    
    db.delete(post)
    db.commit()

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )




