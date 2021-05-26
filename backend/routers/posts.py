import base64
from fastapi import APIRouter, Request, HTTPException, Depends
from starlette.responses import Response
from db.db_main import Session, POSTS, TAGS
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

        tags = []
        files = []
        for tag in post_data.tags:
            tags.append(session.query(TAGS).filter_by(tag_id = tag.id).first())

        print(post_data.images[0].find('base64,'))
        print(post_data.images[0][15 + 7])

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
            tags = tags
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
        print(posts_arr)
        session.close()
    
    if flag:
        return posts_arr


@router.get("/v1/user/posts/count")
def auth_register(user=Depends(manager)):
    return len(user.posts)