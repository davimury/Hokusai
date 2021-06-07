import base64
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy import and_
from db.db_main import Session, USERS, POSTS, TAGS, LIKES, CONNECTIONS, NOTIFICATIONS
from routers.auth import manager
from models import Tags
import pusher
import json

pusher_client = pusher.Pusher(
    app_id="1211691",
    key="ad8252dd0a9b80dd351f",
    secret="1e0679cf8406844cf2f4",
    cluster="us2",
)

router = APIRouter()


@router.get("/profile/suggested")
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
        return Response(status_code=500)


@router.get("/profile/notifications")
async def get_user_notifications(user=Depends(manager)):
    flag = True
    try:
        session = Session()
        notify_arr = []
        notifications = session.query(NOTIFICATIONS).filter_by(
            target_id=user.user_id).all()

        for notification in notifications:
            recipient = session.query(USERS).filter_by(
                user_id=notification.recipient_id).first()
            notify_arr.append(
                {
                    'id': notification.id,
                    'type': 1,
                    'name': recipient.name,
                    'user_id': recipient.user_id,
                    'status': notification.status,
                    'username': recipient.username,
                    'last_updated': notification.last_updated.isoformat()
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


@router.get("/profile/{username}/")
async def get_user_info(username: str, user=Depends(manager)):
    flag = True

    try:
        session = Session()
        connections_arr = [
            *session.query(CONNECTIONS.user_1_id).filter_by(user_2_id = user.user_id).all(),
            *session.query(CONNECTIONS.user_2_id).filter_by(user_1_id = user.user_id).all()
        ]

        posts_arr = []
        tags_arr = []

        this_user = session.query(USERS).filter_by(username=username).first()
        posts = session.query(POSTS).filter_by(post_author=this_user.user_id).order_by(POSTS.post_id.desc()).all()

        if posts:
            tags = session.query(TAGS).filter(TAGS.tag_id.in_(this_user.tags)).all()
        else:
            posts = []
            tags = []
    except Exception as e:
        print(e)
        flag = False

    if flag:
        try:
            for tag in tags:
                tags_arr.append(tag.tag_name)

            for post in posts:
                like_obj = session.query(LIKES).filter_by(
                    post_id=post.post_id, user_id=user.user_id).first()
                like = False
                dislike = False

                if like_obj and like_obj.like_type == True:
                    like = True
                elif like_obj and like_obj.like_type == False:
                    dislike = True

                posts_arr.append({
                    'post_id': post.post_id,
                    'author_id': post.author.user_id,
                    'postType': post.post_type,
                    'description': post.post_body,
                    'slides': post.post_img,
                    'username': post.author.username,
                    'name': post.author.name,
                    'likes': post.likes,
                    'like': like,
                    'dislike': dislike,
                })

        except Exception as e:
            print(e)
            flag = False

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
        }
    else:
        Response(status_code=500)


@router.post("/profile/add/tag")
async def add_tag(tag: Tags, user=Depends(manager)):
    """ Update user favorite tags """
    flag = True

    try:
        session = Session()
        session.expire_on_commit = False

        cur_user = session.query(USERS).filter_by(email=user.email).first()

        if tag.id != None:
            cur_tag = session.query(TAGS).filter_by(tag_id=tag.id).first()
        else:
            cur_tag = session.query(TAGS).filter_by(tag_name=tag.name).first()

        cur_user.add_tag(session, cur_tag.tag_id)
    except:
        flag = False

    finally:
        session.close()

    if flag:
        return Response(status_code=200)
    else:
        return Response(status_code=500)


@router.post("/profile/image")
async def change_profile(request: Request, user=Depends(manager)):
    flag = True
    base = await request.json()

    try:
        filename = str(user.user_id) + ".jpg"

        with open('../frontend/src/assets/img/profile/' + filename, "wb") as f:
            f.write(base64.b64decode(base['base'][base['base'].find(",")+1:]))

    except:
        flag = False

    if flag:
        return Response(status_code=200)
    else:
        return Response(status_code=500)


@router.post("/profile/header")
async def change_header(request: Request, user=Depends(manager)):
    """ Update profile image """
    flag = True
    base = await request.json()

    try:
        filename = str(user.user_id) + ".jpg"

        with open('../frontend/src/assets/img/header/' + filename, "wb") as f:
            f.write(base64.b64decode(base['base'][base['base'].find(",")+1:]))
    except:
        flag = False

    if flag:
        return Response(status_code=200)
    else:
        return Response(status_code=500)


@router.post("/profile/{username}/connect")
async def connection_request(username: str, user=Depends(manager)):
    """ Request connection with other user """
    flag = True
    try:
        session = Session()
        this_user = session.query(USERS).filter_by(username=username).first()

    except Exception as e:
        print(e)
        flag = False

    try:  # Cria uma nova conexão
        connection = session.query(CONNECTIONS).filter_by(user_1_id=this_user.user_id, user_2_id=user.user_id).first()

        if not connection:
            connection = CONNECTIONS(
                con_status=False, user_1_id=user.user_id, user_2_id=this_user.user_id)

            session.add(connection)
            session.commit()

            session.refresh(connection)

            try:    # Cria uma nova notificação destinada ao target_user
                notification = NOTIFICATIONS(
                    type=1,
                    status=False,
                    target_id=this_user.user_id,
                    recipient_id=user.user_id,
                    con_id=connection.con_id
                )
                notification.update_date()
                session.add(notification)
                session.commit()

                session.refresh(notification)
                pusher_client.trigger(
                    'hokusai-notify',
                    this_user.username,
                    {
                        'id': notification.id,
                        'type': 1,
                        'name': user.name,
                        'user_id': user.user_id,
                        'username': user.username,
                        'last_updated': notification.last_updated.isoformat()
                    }
                )
            except Exception as e:
                print(e)
                flag = False
        else:
            notification = session.query(NOTIFICATIONS).filter_by(con_id= connection.con_id).first()
            notification.status = True
            connection.con_status = True

            session.commit()

    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()

    if flag:
        return Response(status_code=200)
    else:
        return Response(status_code=500)


@router.post("/connection/{id}/accept")
async def accept_connection(id: int, user=Depends(manager)):
    """ Request connection with other user """
    flag = True
    try:
        session = Session()
        notification = session.query(NOTIFICATIONS).filter_by(id=id).first()
        connection = session.query(CONNECTIONS).filter_by(con_id=notification.con_id).first()
        
        connection.con_status = True
        notification.status = True
        session.commit()

    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()

    if flag:
        return Response(status_code=200)
    else:
        return Response(status_code=500)


@router.post("/connection/{id}/refuse")
async def refuse_connection(id: int, user=Depends(manager)):
    """ Request connection with other user """
    flag = True
    try:
        session = Session()
        notification = session.query(NOTIFICATIONS).filter_by(id=id).first()
        connection = session.query(CONNECTIONS).filter_by(con_id=notification.con_id).first()
        
        session.delete(notification)
        session.commit()

        session.delete(connection)
        session.commit()
        
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()

    if flag:
        return Response(status_code=200)
    else:
        return Response(status_code=500)
