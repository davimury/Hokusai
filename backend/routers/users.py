import base64
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import and_
from fastapi import APIRouter, Depends, Response, Request
from db.db_main import Session, USERS, POSTS, TAGS, LIKES, CONNECTIONS, NOTIFICATIONS
from routers.auth import manager
from sqlalchemy import or_
from models import Post

router = APIRouter()

# Getters
@router.get("/user/suggested")
async def get_suggested_users(user=Depends(manager)):
    flag = True
    
    try:
        session = Session()
        connections_arr = [
            *session.query(CONNECTIONS.user_1_id).filter_by(user_2_id = user.user_id).all(),
            *session.query(CONNECTIONS.user_2_id).filter_by(user_1_id = user.user_id).all()
        ]

        sugested_array = []
        connected_array = []
        users_arr = []

        for user_id in connections_arr:
            user_ = session.query(USERS).filter_by(user_id= user_id[0]).first()
            connected_array.append(user_)

        if user.tags:
            for tag in user.tags:
                rec_user = session.query(USERS).filter(USERS.tags.contains([tag])).all()
                sugested_array.extend(rec_user)

            s1 = set(sugested_array)
            dif = s1.difference(connected_array)
            
            for user_ in dif:
                if user_.user_id != user.user_id:
                    users_arr.append({
                        'user_id': user_.user_id,
                        'username': user_.username,
                        'name': user_.name,
                    })

    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()

    if flag:
        return users_arr
    else:
        return Response(status_code=404)


@router.get("/user/notifications")
async def get_user_notifications(user=Depends(manager)):
    flag = True
    try:
        session = Session()
        notify_arr = []
        notifications = session.query(NOTIFICATIONS).filter_by(
            target_id=user.user_id).order_by(NOTIFICATIONS.id).all()
        
        if notifications:
            for notification in notifications:
                recipient = session.query(USERS).filter_by(
                    user_id=notification.recipient_id).first()
                notify_arr.append(
                    {
                        'id': notification.id,
                        'type': notification.type,
                        'name': recipient.name,
                        'content': notification.content,
                        'user_id': recipient.user_id,
                        'status': notification.status,
                        'username': recipient.username,
                        'last_updated': notification.last_updated.isoformat(),
                    }
                )

    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()

    if flag:
        return notify_arr
    else:
        return Response(status_code=500)


@router.get("/user/{username}")
async def get_user_info(username: str, user=Depends(manager)):
    flag = True

    try:
        session = Session()
        
        this_user = session.query(USERS).filter_by(username=username).first()
        posts = session.query(POSTS).filter_by(post_author=this_user.user_id).order_by(POSTS.post_id.desc()).all()
        if this_user.tags:
            tags = session.query(TAGS).filter(TAGS.tag_id.in_(this_user.tags)).all()
        else:
            tags = []

        connections_arr = [
            *session.query(CONNECTIONS.user_1_id).filter_by(user_2_id = this_user.user_id).all(),
            *session.query(CONNECTIONS.user_2_id).filter_by(user_1_id = this_user.user_id).all()
        ]
        posts_arr = []
        tags_arr = []

    except Exception as e:
        print(e)
        flag = False

    if flag:
        try:
            for tag in tags:
                tags_arr.append({'tag_id': tag.tag_id, 'name': tag.tag_name})

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

        finally:
            session.close()

    try:
        all_likes = 0
        likes7days = 0

        session = Session()

        for post in this_user.posts:
            all_likes = all_likes + session.query(LIKES).filter(LIKES.post_id == post.post_id).count()
            likes7days = likes7days + session.query(LIKES).filter(and_(LIKES.post_id == post.post_id, LIKES.created_at > datetime.now() - timedelta(days=7))).count()

    except Exception as e:
        flag = False
        print(e)

    finally:
        session.close()

    if flag:
        return {
            'user_id': this_user.user_id,
            'name': this_user.name,
            'tags': tags_arr,
            'posts_count': len(posts_arr),
            'con_count': len(connections_arr),
            'posts': posts_arr,
            'likes7day': likes7days,
            'all_likes': all_likes
        }
    else:
        Response(status_code=500)


@router.get('/user/details/{username}')
async def get_users_info(username: str, user=Depends(manager)):
    flag = True

    try:
        session = Session()

        user_id = session.query(USERS.user_id).filter_by(username = username)
        connections_arr = [
            *session.query(CONNECTIONS.user_1_id).filter_by(user_2_id = user_id).all(),
            *session.query(CONNECTIONS.user_2_id).filter_by(user_1_id = user_id).all()
        ]

    except Exception as e:
        print(e)
        flag = False

    if flag:
        try:
            connections_details = []
            for connection in connections_arr:
                names = session.query(USERS.user_id, USERS.name, USERS.username).filter_by(user_id = connection[0]).first()
                connections_details.append(names)

        except Exception as e:
            print(e)
            flag = False

        finally:
            session.close()

    if flag:
        return {
            'users_details': connections_details,
        }
        
    else:
        Response(status_code=500)

@router.get("/user/search/{query}")
async def get_user_by_query(query: str, user=Depends(manager)):
    try:
        session = Session()
        users_arr = []
        
        users = session.query(USERS).filter(or_(USERS.username.like(f"%{query}%"), USERS.name.like(f"%{query}%"))).all()
        
        for user in users:
            users_arr.append({
                'user_id': user.user_id,
                'username': user.username,
                'name': user.name
            })

    except Exception as e:
        print(e)

    finally:
        return users_arr

#Setters
@router.post("/user/image")
async def change_profile(request: Request, user=Depends(manager)):
    flag = True
    base = await request.json()

    try:
        filename = str(user.user_id) + ".jpg"

        with open('../assets/profile/' + filename, "wb") as f:
            f.write(base64.b64decode(base['base'][base['base'].find(",")+1:]))

    except Exception as e:
        print(e)
        flag = False

    if flag:
        await asyncio.sleep(3)
        return Response(status_code=200)
    else:
        return Response(status_code=500)


@router.post("/user/header")
async def change_header(request: Request, user=Depends(manager)):
    """ Update profile image """
    flag = True
    base = await request.json()

    try:
        filename = str(user.user_id) + ".jpg"

        with open('../assets/header/' + filename, "wb") as f:
            f.write(base64.b64decode(base['base'][base['base'].find(",")+1:]))
    except:
        flag = False

    if flag:
        await asyncio.sleep(1)
        return Response(status_code=200)
    else:
        return Response(status_code=500)




