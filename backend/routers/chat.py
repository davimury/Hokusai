import json
import locale
import pusher
import asyncio
from datetime import datetime
from typing import List, Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from db.db_main import Session, NOTIFICATIONS, USERS, CONNECTIONS, MESSAGES

router = APIRouter()
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

pusher_client = pusher.Pusher(
    app_id="1211691",
    key="ad8252dd0a9b80dd351f",
    secret="1e0679cf8406844cf2f4",
    cluster="us2",
)

class UserManager:
    def __init__(self):
        self.connection: WebSocket = None
        self.broadcaster: ChatBroadcaster = None
        self.user = None
        self.rooms = []
        self.messages = []
        self.current_room = None
        self.target_id = None
        self.counter = 0

    async def load_user(self, ws, user_id, broadcaster):
        try:
            self.connection = ws
            self.broadcaster = broadcaster
            await self.connection.accept()

            session = Session()
            self.user = session.query(USERS).filter_by(user_id=user_id).first().__dict__
            session.close()
        
        except Exception as e:
            print(e)
        
        finally:
            await self.get_user_rooms()

    async def request_handler(self, data):
        if data:
            parsed_data = json.loads(data)
            if 'get_messages' in parsed_data:
                await self.get_room_msg(parsed_data['get_messages'], parsed_data['query'])
            
            elif 'send_message' in parsed_data:
                await self.send_message(parsed_data['send_message'])
            
            elif 'edit_message' in parsed_data:
                await self.edit_message(parsed_data['edit_message'])
    
            elif 'delete_message' in parsed_data:
                await self.delete_message(parsed_data['delete_message'])
    
    async def get_user_rooms(self):
        try:
            session = Session()

            connections_arr = [
                *session.query(CONNECTIONS).filter_by(user_2_id=self.user['user_id'], con_status=True).all(),
                *session.query(CONNECTIONS).filter_by(user_1_id=self.user['user_id'], con_status=True).all()
            ]

            for con in connections_arr:
                sender = session.query(USERS).filter_by(user_id=self.user['user_id']).first()
                target = session.query(USERS).filter_by(user_id=con.get_connected_user(self.user['user_id'])).first()
                last_message = session.query(MESSAGES).filter_by(con_id=con.con_id).order_by(MESSAGES.message_id.desc()).first()

                self.rooms.append({
                    'roomId': con.con_id,
                    'roomName': target.name,
                    'avatar': f"{target.user_id}.jpg",
                    'unreadCount': 0,
                    'index': datetime.timestamp(last_message.created_at) if last_message else 0,
                    'lastMessage': {
                        'content': last_message.content,
                        'senderId': last_message.sender_id,
                        'username': last_message.user.username,
                        'timestamp': "{:d}:{:02d}".format(last_message.created_at.hour, last_message.created_at.minute),
                        'saved': True,
                        'distributed': True,
                        'seen': last_message.seen,
                        'new': True,
                    } if last_message else {
                        'content': '',
                        'senderId': '',
                        'username': '',
                        'timestamp': '',
                        'saved': False,
                        'distributed': False,
                        'seen': '',
                        'new': False,
                    },
                    'users': [
                        {
                            '_id': sender.user_id,
                            'username': sender.name,
                            'avatar': f"{sender.user_id}.jpg",
                            'status': {
                                'state': "online" if sender.user_id in self.broadcaster.online_users else "offline",
                                'lastChanged': "",
                            },
                        },
                        {
                            '_id': target.user_id,
                            'username': target.name,
                            'avatar': f"{target.user_id}.jpg",
                            'status': {
                                'state': "online" if target.user_id in self.broadcaster.online_users else "offline",
                                'lastChanged': "",
                            },
                        },
                    ],
                    'typingUsers': [],
                })

            session.close()

        except Exception as e:
            print(e)

        finally:
            await self.connection.send_text(json.dumps({'rooms': self.rooms}))

    async def get_room_msg(self, con_id, query):
        try:
            session = Session()
            self.messages = []
            self.current_room = session.query(CONNECTIONS).filter_by(con_id=con_id).first()
            self.second_user = session.query(USERS).filter_by(user_id=self.current_room.get_connected_user(self.user['user_id'])).first()

        except Exception as e:
            print(e)
            session.rollback()
        
        finally:
            session.close()

        try:
            session = Session()

            messages_arr = session.query(MESSAGES).filter_by(con_id=self.current_room.con_id).order_by(MESSAGES.created_at.asc()).all()
            output = list(reversed([messages_arr[i:i + 15] for i in range(0, len(messages_arr), 15)]))

            flag = False
            for message in messages_arr:
                if message.seen == False:
                    flag = True

            if flag:
                await self.seen_room()

        except Exception as e:
            print(e)
            session.rollback()
        
        finally:
            session.close()

        if len(output) > query:
            for msg in output[query]:
                try:
                    session = Session()

                    user = session.query(USERS).filter_by(
                        user_id=msg.sender_id).first()
                    
                    if msg.seen == False and msg.sender_id != self.user['user_id']:
                        msg.seen_message()
                        session.merge(msg)
                        session.commit()

                        await self.broadcaster.broadcast_to_user(self.second_user.user_id, {'seen_msg': {'id': msg.message_id}})

                    if msg.reply_id:
                        reply_message = session.query(MESSAGES).filter_by(message_id=msg.reply_id).first()

                    self.messages.append({
                        '_id': msg.message_id,
                        'content': msg.content,
                        'index': datetime.timestamp(msg.created_at) if msg else 0,
                        'senderId': msg.sender_id,
                        'username': user.username,
                        'avatar': f"{user.user_id}.jpg",
                        'date': "%s %s" % (msg.created_at.day, msg.created_at.strftime("%B")),
                        'timestamp': "{:d}:{:02d}".format(msg.created_at.hour, msg.created_at.minute),
                        'system': False,
                        'saved': True,
                        'distributed': True,
                        'seen': msg.seen,
                        'disableActions': False,
                        'disableReactions': False,
                        'reactions': {},
                        'replyMessage': {
                            '_id': reply_message.message_id,
                            'content': reply_message.content,
                            'sender_id': reply_message.sender_id
                        } if msg.reply_id else None,
                    })

                except Exception as e:
                    print(e)
                    session.rollback()

                finally:
                    session.close()
            

        else:
            self.messages = []
        
        try:
            await self.connection.send_text(json.dumps({'messages': self.messages}))

        except Exception as e:
            print(e)

    async def send_message(self, message):
        try:
            session = Session()

            new_message = MESSAGES(
                con_id = message['room_id'],
                sender_id = message['sender_id'],
                content = message['content'],
                seen = False,
                reply_id = message['reply_message']['_id'] if message['reply_message'] else None,
            )

            new_message.update_date()
            session.add(new_message)
            session.commit()

            session.refresh(new_message)
            session.close()

            await self.send_msg_notification(message['room_id'])

            final_message = {
                'new_message': {
                    '_id': new_message.message_id,
                    'content': new_message.content,
                    'senderId': new_message.sender_id,
                    'username': self.user['username'],
                    'avatar': f"{self.user['user_id']}.jpg",
                    'date': "%s %s" % (new_message.created_at.day, new_message.created_at.strftime("%B")),
                    'timestamp': "{:d}:{:02d}".format(new_message.created_at.hour, new_message.created_at.minute),
                    'system': False,
                    'saved': True,
                    'distributed': True,
                    'seen': new_message.seen,
                    'disableActions': False,
                    'disableReactions': False,
                    'reactions': {},
                    'replyMessage': { 
                        '_id': message['reply_message']['_id'], 
                        'content':message['reply_message']['content'], 
                        'sender_id': message['reply_message']['senderId'] 
                    } if message['reply_message'] else None
                }
            }

            await self.broadcaster.broadcast_to_user(self.current_room.get_connected_user(new_message.sender_id), final_message)
            await self.connection.send_text(json.dumps(final_message))

        except Exception as e:
            print(e)

    async def edit_message(self, message):
        try:
            session = Session()
            message_obj = session.query(MESSAGES).filter_by(message_id=message['messageId']).first()

            message_obj.content = message['new_content']
            if message['reply_message']:
                message_obj.reply_id = message['reply_message']['_id']

            session.merge(message_obj)
            session.commit()

            await self.broadcaster.broadcast_edit_msg(self.user['user_id'], message_obj)

        except Exception as e:
            print(e)
        
        finally:
            session.close()

    async def delete_message(self, message):
        try:
            session = Session()
            message_obj = session.query(MESSAGES).filter_by(message_id=message['_id']).first()

            session.delete(message_obj)
            session.commit()

            await self.broadcaster.broadcast_delete_msg(self.user['user_id'], message_obj)

        except Exception as e:
            print(e)
        
        finally:
            session.close()

    async def send_msg_notification(self, con_id):
        try:
            session = Session()
            connection = session.query(CONNECTIONS).filter_by(con_id = con_id).first() 
            self.target_id = connection.get_connected_user(self.user['user_id'])

            if not await self.broadcaster.is_online(self.target_id):
                notification = session.query(NOTIFICATIONS).filter_by(target_id = self.target_id, recipient_id = self.user['user_id'], type = 0).first()
                messages_count = session.query(MESSAGES).filter_by(sender_id = self.user['user_id'], con_id = con_id, seen=False).count()

                if not notification:
                    notification = NOTIFICATIONS(
                        target_id=connection.get_connected_user(self.user['user_id']),
                        recipient_id=self.user['user_id'],
                        con_id=con_id,
                        type=0,
                        status=False,
                        content={'count': messages_count}
                    ) 

                    notification.update_date()
                    session.add(notification)
                    session.commit()

                else:
                    notification.content = {'count': messages_count}
                    notification.status = False
                    notification.update_date()
                    session.merge(notification)
                    session.commit()

                pusher_client.trigger(
                    'hokusai-notify',
                    session.query(USERS.username).filter_by(user_id=self.target_id).first()[0],
                    {
                        'id': notification.id,
                        'type': notification.type,
                        'status': notification.status,
                        'name': self.user['name'],
                        'user_id': self.user['user_id'],
                        'username': self.user['username'],
                        'content': {'count': messages_count},
                        'last_updated': notification.last_updated.isoformat()
                    }
                )

        except Exception as e:
            print(e)
            session.rollback()

        finally:
            session.close()

    async def seen_room(self):
        try:
            session = Session()
        except Exception as e:
            print(e)

        try:
            notification = session.query(NOTIFICATIONS).filter_by(target_id=self.user['user_id'], type = 0, con_id=self.current_room.con_id).first()
            
            if notification:
                notification.seen_notification()
                notification.content = {'count': 0}
                session.merge(notification)
                session.commit()

        except Exception as e:
            print(e)
        
        try:
            await asyncio.sleep(1)
            pusher_client.trigger(
                'hokusai-notify',
                self.user['username'],
                {
                    'id': notification.id,
                    'type': notification.type,
                    'status': notification.status,
                    'name': self.second_user.name,
                    'user_id': self.second_user.user_id,
                    'username': self.second_user.username,
                    'content': notification.content,
                    'last_updated': notification.last_updated.isoformat()
                })
        except Exception as e:
            print(e)

class ChatBroadcaster:
    def __init__(self):
        self.connections: List[Dict(int, WebSocket)] = []
        self.online_users: List[int] = []

    async def is_online(self, user_id):
        for con in self.connections:
            if user_id == list(con.keys())[0]:
                return True
            
        return False

    async def register_connection(self, ws, client_id):
        self.connections.append({client_id: ws})
        self.online_users.append(client_id)
        await self.broadcast_status(client_id, True)

    async def remove_connection(self, client_id):
        for idx, con in enumerate(self.connections):
            if client_id in con:
                self.online_users.remove(client_id)
                self.connections.remove(self.connections[idx])
        
        await self.broadcast_status(client_id, False)

    async def broadcast_to_user(self, user_id, message):
        for con in self.connections:
            if user_id in con:
                await con[user_id].send_text(json.dumps(message))

                if "new_message" in message:
                    if message["new_message"]["senderId"] != user_id:
                        await self.broadcast_seen_msg(message, user_id)
                
    async def broadcast_seen_msg(self, message, user_id):
        try:
            session = Session()
            message_obj = session.query(MESSAGES).filter_by(message_id= message['new_message']['_id']).first()
            
            if message_obj.seen == False:
                message_obj.seen_message()
                session.merge(message_obj)
                session.commit()

        except Exception as e:
            print(e)
            session.rollback()

        finally:
            session.close()

        try:
            session = Session()
            connections_arr = [
                    *session.query(CONNECTIONS).filter_by(user_2_id=user_id).all(),
                    *session.query(CONNECTIONS).filter_by(user_1_id=user_id).all()
                ]
            
            for con in connections_arr:
                await self.broadcast_to_user(con.get_connected_user(user_id), {'seen_msg': {'id': message['new_message']['_id']}})
            
        except Exception as e:
            print(e)
            session.rollback()
        
        finally:
            session.close()

    async def broadcast_status(self, client_id, status):
        try:
            session = Session()
            connections_arr = [
                    *session.query(CONNECTIONS).filter_by(user_2_id=client_id).all(),
                    *session.query(CONNECTIONS).filter_by(user_1_id=client_id).all()
                ]
            
            for con in connections_arr:
                await self.broadcast_to_user(
                    con.get_connected_user(client_id), 
                        {
                            'user_status': 
                            {
                                'id': client_id, 
                                'status': status
                            }
                        }
                )
            
        except:
            session.rollback()
        
        finally:
            session.close()

    async def broadcast_edit_msg(self, client_id, new_message):
        try:
            session = Session()
            connections_arr = [
                    *session.query(CONNECTIONS).filter_by(user_2_id=client_id).all(),
                    *session.query(CONNECTIONS).filter_by(user_1_id=client_id).all()
                ]

            for con in connections_arr:
                await self.broadcast_to_user(con.get_connected_user(client_id), {'edit_msg': {'_id': new_message.message_id, 'content': new_message.content}})
            
            await self.broadcast_to_user(client_id, {'edit_msg': {'_id': new_message.message_id, 'content': new_message.content}})

        except:
            pass

        finally:
            session.close()

    async def broadcast_delete_msg(self, client_id, deleted_message):
        try:
            session = Session()
            connections_arr = [
                    *session.query(CONNECTIONS).filter_by(user_2_id=client_id).all(),
                    *session.query(CONNECTIONS).filter_by(user_1_id=client_id).all()
                ]

            for con in connections_arr:
                await self.broadcast_to_user(con.get_connected_user(client_id), {'delete_msg': {'_id': deleted_message.message_id}})
            
            await self.broadcast_to_user(client_id, {'delete_msg': {'_id': deleted_message.message_id}})

        except:
            pass

        finally:
            session.close()

broadcaster = ChatBroadcaster()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    manager = UserManager()

    await broadcaster.register_connection(websocket, client_id)
    await manager.load_user(websocket, client_id, broadcaster)

    try:
        while True:
            data = await manager.connection.receive_text()
            await manager.request_handler(data)

    except WebSocketDisconnect:
        await broadcaster.remove_connection(client_id)
        del manager
        
        
