import base64
from fastapi import APIRouter, Request, HTTPException, Depends
from starlette.responses import Response
from db.db_main import Session, POSTS, TAGS, USERS, LIKES
from datetime import datetime
from sqlalchemy import and_
from models import Posts
from routers.login import manager

router = APIRouter()

@router.get("/v1/posts/")
def get_user_posts(user=Depends(manager)):
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
            like_obj = session.query(LIKES).filter_by(post_id = post.post_id, user_id=user.user_id).first()
            like = False
            dislike = False

            if like_obj and like_obj.like_type == True:
                like = True
            elif like_obj and like_obj.like_type == False:
                dislike = True
            
            posts_arr.append({
                'post_id': post.post_id,
                'description': post.post_body,
                'slides': post.post_img,
                'username': post.author.username,
                'author_id': post.author.user_id,
                'postType': post.post_type,
                'likes': post.likes,
                'like': like,
                'dislike': dislike,
            })
                
        return posts_arr

@router.get("/v1/post/{username}")
def get_posts(username: str):
    """ Retorna um post especifico """
    """ Retorna todos posts de um user """
    try:
        flag = True
        session = Session()

        user_id = session.query(USERS.user_id).filter_by(username = username).first()
        posts = session.query(POSTS).filter_by(post_author=user_id).order_by(POSTS.post_id.desc()).all()
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
def new_post(post_data:Posts, user=Depends(manager)):
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

@router.post("/v1/post/{id}/like")
def like_post(id: int, user=Depends(manager)):
    try:
        flag = True
        session = Session()

        like = session.query(LIKES).filter_by(post_id = id, user_id=user.user_id).first()

        if not like:
            like = LIKES(user_id=user.user_id, post_id=id, like_type=True)
            session.add(like)
        else:
            like.like_type = True

        like.update_date()
        like_count = session.query(LIKES).filter(and_(LIKES.post_id == id, LIKES.like_type == True)).count()
        post = session.query(POSTS).filter_by(post_id = id).first()
        post.likes = like_count

        session.commit()
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()
    
    if flag:
        return like_count

@router.post("/v1/post/{id}/dislike")
def dislike_post(id: int, user=Depends(manager)):
    try:
        flag = True
        session = Session()

        like = session.query(LIKES).filter_by(post_id = id, user_id=user.user_id).first()

        if not like:
            like = LIKES(user_id=user.user_id, post_id=id, like_type=False)
            session.add(like)
        else:
            like.like_type = False
        
        like.update_date()
        like_count = session.query(LIKES).filter(and_(LIKES.post_id == id, LIKES.like_type == True)).count()
        post = session.query(POSTS).filter_by(post_id = id).first()
        post.likes = like_count

        session.commit()
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()
    
    if flag:
        return like_count
