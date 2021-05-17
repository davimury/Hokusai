from fastapi import APIRouter, Request, HTTPException, Depends
from starlette.responses import Response
from db.db_main import Session, POSTS
from datetime import datetime
from sqlalchemy import exc
from models import Posts
from routers.login import manager

router = APIRouter()

@router.get("/v1/posts/")
def auth_register(user=Depends(manager)):
    """ Retorna todos posts de um user """
    try:
        flag = True
        session = Session()

        posts = session.query(POSTS).filter_by(post_author=user.user_id).order_by(POSTS.post_id.desc()).all()

    except Exception as e:
        print(e)
        flag = False
        #raise HTTPException(status_code=409, detail="email ou username já cadastrados!")
    
    finally:
        session.close()
        
    if flag: 
        posts_arr = []

        for post in posts:
            posts_arr.append({
                'post_id': post.post_id,
                'description': post.post_body,
                'slides': post.post_img,
                'profile_picture': "https://picsum.photos/id/1027/150/150",
                'username': post.author.name,
                'postType': 1,
            })
        
        return posts_arr

@router.get("/v1/post/{post_id}")
def auth_register(post_id: int, user=Depends(manager)):
    """ Retorna um post especifico """
    print(post_id)

@router.post("/v1/new_post/")
def auth_register(post_data:Posts, user=Depends(manager)):
    """ Adiciona um novo post """
    try:
        flag = True
        session = Session()

        new_post = POSTS(
            post_author = user.user_id,
            post_body = post_data.body,
            post_img = post_data.images,
            post_reactions = post_data.reactions,
            created_at = datetime.now()
        )

        session.add(new_post)
        session.commit()
        
    except Exception as e:
        print(e)
        flag = False
        #raise HTTPException(status_code=409, detail="email ou username já cadastrados!")
    
    finally:
        session.close()
        
    if flag: 
        return Response(status_code=200)
