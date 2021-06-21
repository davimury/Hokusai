import base64
import string
import random
from sqlalchemy import and_
from fastapi.exceptions import HTTPException
from db.db_main import Session, POSTS, TAGS, LIKES, CONNECTIONS
from datetime import datetime, timedelta
from starlette.responses import JSONResponse, Response
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi import APIRouter, Depends, Request
from routers.auth import manager
from models import Post


router = APIRouter()


# Getters
@router.get("/posts/by_tag/{tag}")
def get_posts_by_tag(tag: str, user=Depends(manager)):
    """ Retorna todos posts por tag """
    try:
        session = Session()
        tag_obj = session.query(TAGS).filter_by(tag_name=tag).first()

        posts_arr = []

        if tag_obj:
            posts = tag_obj.posts
        else:
            return Response(status_code=404)
        
        
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

    except Exception as e:
        print(e)

    finally:
        session.close()



@router.get("/posts/recommended/{query}")
def get_recommended_posts(query: int, user=Depends(manager)):
    """ Retorna todos posts do user logado user """
    try:
        flag = True
        session = Session()
        week = datetime.today() - timedelta(days=7)

        posts = session.query(POSTS).filter(POSTS.created_at > week).order_by(POSTS.likes.desc()).all()
    
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()

    if flag:
        try:
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

        except Exception as e:
            print(e)
            flag = False

        try:
            output = [posts_arr[i:i + 3] for i in range(0, len(posts_arr), 3)]
            return output[query]
        except:
            return None


@router.get("/posts/connections/{query}")
def get_connections_posts(query: int, user=Depends(manager)):
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
        try:
            posts_arr = sorted(posts_arr, key=lambda x: x.created_at, reverse=True)
            output = [posts_arr[i:i + 3] for i in range(0, len(posts_arr), 3)]
            return output[query]
        except:
            return None


#Setters
@router.post("/post/new")
def new_post(post: Post, user=Depends(manager)):
    """ Adiciona um novo post """
    try:
        flag = True
        session = Session()
        tags = []
    
        try:
            print(post.description)
            for tag in post.tags:
                tags.append(session.query(TAGS).filter_by(tag_id=tag.tag_id).first())
        except Exception as e:
            print(e)
        
        if post.postType == 0:
            if post.slides:
                new_post = POSTS(
                    author=user,
                    post_author=user.user_id,
                    post_desc=post.description,
                    post_img=post.slides,
                    post_type=post.postType,
                    created_at=datetime.now(),
                    tags=tags,
                    likes=0,
                )

                session.add(new_post)
                session.commit()
            
            else:
                raise HTTPException(status_code=404)

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

        session.refresh(new_post)

    except Exception as e:
        print(e)
        flag = False
        return Response(status_code=500)

    finally:
        session.close()

    if flag:
        return JSONResponse(content={'post_id': new_post.post_id})


@router.post("/post/new/image")
async def new_image(file: UploadFile = File(...)):
    """ Adiciona um novo post """
    try:
        flag = True
        
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)).replace("/", "") + str(
                    datetime.now().second * datetime.now().day) + ".jpg"
                    
        file_location = f"../assets/posts/{filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

    except Exception as e:
        print(e)
        flag = False
        return Response(status_code=500)

    if flag:
        return {"filename": filename}



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

@router.get("/post/statistics")
def statistics_get(request: Request, user=Depends(manager)):  
    try:
        session = Session()
        upvotes_week_ago = []
        downvotes_week_ago = []
        week_ago = datetime.now() - timedelta(days=7)
        posts = session.query(POSTS).filter(and_(POSTS.post_author == user.user_id)).all()
        print(posts)
        for post in posts:
            for like in (session.query(LIKES.created_at).filter(and_(LIKES.post_id == post.post_id, LIKES.like_type == True, LIKES.created_at > week_ago)).all()):
                if like[0]:
                    upvotes_week_ago.append((like[0].weekday() + 1) % 7) #conta para primeiro dia da semana começar no domingo
            for dislike in (session.query(LIKES.created_at).filter(and_(LIKES.post_id == post.post_id, LIKES.like_type == False, LIKES.created_at > week_ago)).all()):
                if dislike[0]:
                    downvotes_week_ago.append((dislike[0].weekday() + 1) % 7) #conta para primeiro dia da semana começar no domingo
        
        
        return JSONResponse(content={'upvotes_week_ago':upvotes_week_ago, 'downvotes_week_ago':downvotes_week_ago})
    except Exception as e:
        print(e)

    finally:
        session.close() 
