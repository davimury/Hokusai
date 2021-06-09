import pusher
from db.db_main import Session, USERS, CONNECTIONS, NOTIFICATIONS
from fastapi import APIRouter, Depends, Response
from routers.auth import manager
from models import User, Connection

pusher_client = pusher.Pusher(
    app_id="1211691",
    key="ad8252dd0a9b80dd351f",
    secret="1e0679cf8406844cf2f4",
    cluster="us2",
)

router = APIRouter()

@router.get('/connection/{username}')
async def is_connected(username: str, user=Depends(manager)):
    flag = True
    try:
        is_connected = False
        con_status = None

        session = Session()
        
        this_user = session.query(USERS).filter_by(username=username).first()
        connections_arr = [
            *session.query(CONNECTIONS.user_1_id, CONNECTIONS.con_status).filter_by(user_2_id = user.user_id).all(),
            *session.query(CONNECTIONS.user_2_id, CONNECTIONS.con_status).filter_by(user_1_id = user.user_id).all()
        ]

        for con in connections_arr:
            if con[0] == this_user.user_id:
                is_connected = True
                con_status = con[1]
        
        print(con_status)
    except Exception as e:
        print(e)
        flag = False

    finally:
        session.close()
        return {'is_connected': is_connected, 'con_status': con_status}

@router.post("/connection/new")
async def connection_request(target: User, user=Depends(manager)):
    """ Request connection with other user """
    flag = True
    try:
        session = Session()
        this_user = session.query(USERS).filter_by(username=target.username).first()

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


@router.post("/connection/accept")
async def accept_connection(con: Connection, user=Depends(manager)):
    """ Request connection with other user """
    flag = True
    try:
        session = Session()
        notification = session.query(NOTIFICATIONS).filter_by(id=con.con_id).first()
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


@router.post("/connection/refuse")
async def refuse_connection(con: Connection, user=Depends(manager)):
    """ Request connection with other user """
    flag = True
    try:
        session = Session()
        notification = session.query(NOTIFICATIONS).filter_by(id=con.con_id).first()
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
