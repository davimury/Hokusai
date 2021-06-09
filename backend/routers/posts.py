import base64
from db.db_main import Session, POSTS, TAGS, LIKES, CONNECTIONS
from datetime import datetime, timedelta
from starlette.responses import Response
from fastapi import APIRouter, Depends
from routers.auth import manager
from models import Post, Tag
from sqlalchemy import and_


router = APIRouter()


# Getters
@router.get("/posts/by_tag")
def get_posts_by_tag(tag: Tag, user=Depends(manager)):
    """ Retorna todos posts do user logado user """
    try:
        flag = True
        session = Session()
        tag_arr = []

        for tag in user.tags:
            tag = tag_arr.append(session.query(TAGS).filter_by(tag_id=tag).first())

        posts = session.query(POSTS).filter(POSTS.tags.contains(*tag_arr)).all()

    except Exception as e:
        print(e)
        flag = False
        #raise HTTPException(status_code=409, detail="email ou username já cadastrados!")

    finally:
        session.close()

    if flag:
        posts_arr = []

        for post in posts:
            like_obj = session.query(LIKES).filter_by(
                post_id=post.post_id, user_id=user.user_id).first()
            like = False
            dislike = False

            if like_obj and like_obj.like_type == True:
                like = True
            elif like_obj and like_obj.like_type == False:
                dislike = True

            posts_arr.append(Posts(**{
                'post_id': post.post_id,
                'description': post.post_body,
                'slides': post.post_img,
                'username': post.author.username,
                'author_id': post.author.user_id,
                'postType': post.post_type,
                'created_at': post.created_at,
                'likes': post.likes,
                'like': like,
                'dislike': dislike,
            }))

        return posts_arr


@router.get("/posts/recommended")
def get_recommended_posts(user=Depends(manager)):
    """ Retorna todos posts do user logado user """
    try:
        flag = True
        session = Session()
        week = datetime.today() - timedelta(days=7)

        posts = session.query(POSTS).filter(POSTS.created_at > week).order_by(POSTS.likes.desc()).limit(50).all()
    except Exception as e:
        print(e)
        flag = False
        #raise HTTPException(status_code=409, detail="email ou username já cadastrados!")

    finally:
        session.close()

    if flag:
        posts_arr = []

        for post in posts:
            like_obj = session.query(LIKES).filter_by(
                post_id=post.post_id, user_id=user.user_id).first()
            like = False
            dislike = False

            if like_obj and like_obj.like_type == True:
                like = True
            elif like_obj and like_obj.like_type == False:
                dislike = True

            posts_arr.append(Post(**{
                'post_id': post.post_id,
                'body': post.post_body,
                'description': post.post_desc,
                'slides': post.post_img,
                'username': post.author.username,
                'author_id': post.author.user_id,
                'postType': post.post_type,
                'created_at': post.created_at,
                'likes': post.likes,
                'like': like,
                'dislike': dislike,
            }))

        return posts_arr


@router.get("/posts/connections")
def get_connections_posts(user=Depends(manager)):
    """ Retorna um post especifico """
    try:
        flag = True
        session = Session()
        posts_arr = []

        following_list = [
            *session.query(CONNECTIONS.user_1_id).filter_by(user_2_id = user.user_id).all(),
            *session.query(CONNECTIONS.user_2_id).filter_by(user_1_id = user.user_id).all()
        ]

        for user_id in following_list:
            posts = session.query(POSTS).filter_by(post_author = user_id[0]).all()

            if posts:
                for post in posts:
                    like_obj = session.query(LIKES).filter_by(
                        post_id=post.post_id, user_id=user.user_id).first()
                    like = False
                    dislike = False

                    if like_obj and like_obj.like_type == True:
                        like = True
                    elif like_obj and like_obj.like_type == False:
                        dislike = True

                    posts_arr.append(Post(**{
                        'post_id': post.post_id,
                        'body': post.post_body,
                        'description': post.post_desc,
                        'slides': post.post_img,
                        'username': post.author.username,
                        'author_id': post.author.user_id,
                        'postType': post.post_type,
                        'created_at': post.created_at,
                        'likes': post.likes,
                        'like': like,
                        'dislike': dislike,
                    }))

    except Exception as e:
        print(e)
        flag = False
        #raise HTTPException(status_code=409, detail="email ou username já cadastrados!")

    finally:
        session.close()

    if flag:
        return posts_arr


#Setters
@router.post("/post/new")
def new_post(post: Post, user=Depends(manager)):
    """ Adiciona um novo post """
    try:
        flag = True
        session = Session()
        
        tags = []

        for tag in post.tags:
            tags.append(session.query(TAGS).filter_by(tag_id=tag.tag_id).first())
        
        if post.postType == 0:
            files = []

            for image in post.slides:
                filename = str(user.user_id) + image[150:155].replace("/", "") + str(
                    datetime.now().second * datetime.now().day) + ".jpg"
                files.append(filename)

                with open('../frontend/src/assets/img/posts/' + filename, "wb") as f:
                    f.write(base64.b64decode(image[image.find(",")+1:]))

            new_post = POSTS(
                author=user,
                post_author=user.user_id,
                post_desc=post.description,
                post_img=files,
                post_type=post.postType,
                created_at=datetime.now(),
                tags=tags,
                likes=0,
            )

            session.add(new_post)
            session.commit()

        else:
            new_post = POSTS(
                author=user,
                post_author=user.user_id,
                post_body=post.body,
                post_desc=post.description,
                post_type=post.postType,
                created_at=datetime.now(),
                tags=tags,
                likes=0,
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


@router.post("/post/like")
def like_post(post: Post, user=Depends(manager)):
    flag = True

    try:
        
        session = Session()

        like = session.query(LIKES).filter_by(
            post_id=post.post_id, user_id=user.user_id).first()

        if not like:
            like = LIKES(user_id=user.user_id, post_id=post.post_id, like_type=True)
            session.add(like)
        else:
            like.like_type = True

        like.update_date()
        like_count = session.query(LIKES).filter(
            and_(LIKES.post_id == post.post_id, LIKES.like_type == True)).count()
        post = session.query(POSTS).filter_by(post_id=post.post_id).first()
        post.likes = like_count

        session.commit()
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()

    if flag:
        return like_count


@router.post("/post/dislike")
def dislike_post(post: Post, user=Depends(manager)):
    flag = True

    try:
        session = Session()

        like = session.query(LIKES).filter_by(
            post_id=post.post_id, user_id=user.user_id).first()

        if not like:
            like = LIKES(user_id=user.user_id, post_id=post.post_id, like_type=False)
            session.add(like)
        else:
            like.like_type = False

        like.update_date()
        like_count = session.query(LIKES).filter(
            and_(LIKES.post_id == post.post_id, LIKES.like_type == True)).count()
        post = session.query(POSTS).filter_by(post_id=post.post_id).first()
        post.likes = like_count

        session.commit()
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()

    if flag:
        return like_count
