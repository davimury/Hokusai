import base64
from fastapi import APIRouter, Request, HTTPException, Depends
from starlette.responses import Response
from db.db_main import Session, POSTS, TAGS, USERS
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
        print(posts)
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
                'username': post.author.username,
                'author_id': post.author.user_id,
                'postType': post.post_type,
                'likes': post.likes,
            })
        
        return posts_arr

@router.get("/v1/post/{username}")
def auth_register(username: str):
    """ Retorna um post especifico """
    """ Retorna todos posts de um user """
    try:
        flag = True
        session = Session()

        user_id = session.query(USERS.user_id).filter_by(username = username).first()
        posts = session.query(POSTS).filter_by(post_author=user_id).order_by(POSTS.post_id.desc()).all()
        print(posts)
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
                'username': post.author.username,
                'name': post.author.name,
                'author_id': post.author.user_id,
                'postType': post.post_type,
                'likes': post.likes,
            })
        
        return posts_arr

@router.post("/v1/new_post/")
def auth_register(post_data:Posts, user=Depends(manager)):
    """ Adiciona um novo post """
    try:
        flag = True
        session = Session()

        tags = []
        files = []
        for tag in post_data.tags:
            tags.append(session.query(TAGS).filter_by(tag_id = tag.id).first())

        for image in post_data.images:
            filename = str(user.user_id) + image[150:155].replace("/", "") + str(datetime.now().second * datetime.now().day) + ".jpg"
            files.append(filename)

            with open('../frontend/src/assets/img/posts/' + filename, "wb") as f:
                f.write(base64.b64decode(image[image.find(",")+1:]))

        new_post = POSTS(
            author = user,
            post_author = user.user_id,
            post_body = post_data.body,
            post_img = files,
            post_type = post_data.type,
            created_at = datetime.now(),
            tags = tags,
            likes = 0,
        )

        session.add(new_post)
        session.commit()
        
    except Exception as e:
        print(e)
        flag = False
        return Response(status_code=500)
        #raise HTTPException(status_code=409, detail="email ou username já cadastrados!")
    
    finally:
        session.close()
        
    if flag: 
        return Response(status_code=200)


@router.get("/v1/user/{id}/posts")
def auth_register(id: int, user=Depends(manager)):
    posts_arr = [];
    try:
        flag = True
        session = Session()

        posts = session.query(POSTS).filter_by(post_author = id).all()
        for post in posts:
            posts_arr.append({
                'post_id': post.post_id,
                'description': post.post_body,
                'slides': post.post_img,
                'username': post.author.username,
                'author_id': post.post_author,
                'postType': post.post_type,
            })
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()
    
    if flag:
        return posts_arr


@router.get("/v1/user/posts/count")
def auth_register(user=Depends(manager)):
    return len(user.posts)

@router.get("/v1/post/{id}/likes")
def auth_register(id: int):
    try:
        flag = True
        session = Session()

        post = session.query(POSTS).filter_by(post_id = id).first()
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()
    
    if flag:
        return post.likes

@router.post("/v1/post/{id}/like")
def like_post(id: int):
    try:
        flag = True
        session = Session()

        post = session.query(POSTS).filter_by(post_id = id).first()

        if post.likes != None:
            post.likes = post.likes + 1
        else:
            post.likes = 1

        session.commit()
        session.refresh(post)
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()
    
    if flag:
        return post.likes

@router.post("/v1/post/{id}/dislike")
def like_post(id: int):
    try:
        flag = True
        session = Session()

        post = session.query(POSTS).filter_by(post_id = id).first()

        if post.likes != None and post.likes > 0:
            post.likes = post.likes - 1
        else:
            post.likes = 0

        session.commit()
        session.refresh(post)
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()
    
    if flag:
        return post.likes
