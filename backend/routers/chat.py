import json
from sqlalchemy import event
from typing import List, Dict, Optional
from fastapi import APIRouter, WebSocket
from models import User
from db.db_main import db_engine, Session, USERS, CONNECTIONS, MESSAGES

router = APIRouter()

class UserManager:
    def __init__(self):
        self.connection = None
        self.broadcaster = None
        self.user = None
        self.rooms = []
        self.messages = []
        self.current_room = None

    async def load_user(self, ws, user_id, broadcaster):
        try:
            self.connection = ws
            self.broadcaster = broadcaster
            await self.connection.accept()

            session = Session()
            self.user = session.query(USERS).filter_by(user_id=user_id).first().__dict__
            session.close()
        except:
            pass
        
        finally:
            await self.get_user_rooms()

    async def request_handler(self, data):
        if data:
            parsed_data = json.loads(data)
            if 'get_messages' in parsed_data:
                await self.get_room_msg(parsed_data['get_messages'])
            
            elif 'send_message' in parsed_data:
                await self.send_message(parsed_data['send_message'])
    
    async def get_user_rooms(self):
        try:
            session = Session()
            connections_arr = [
                *session.query(CONNECTIONS).filter_by(user_2_id=self.user['user_id']).all(),
                *session.query(CONNECTIONS).filter_by(user_1_id=self.user['user_id']).all()
            ]

            for con in connections_arr:
                sender = session.query(USERS).filter_by(user_id=self.user['user_id']).first()
                target = session.query(USERS).filter_by(user_id=con.get_connected_user(self.user['user_id'])).first()

                self.rooms.append({
                    'roomId': con.con_id,
                    'roomName': target.name,
                    'avatar': f"assets/img/profile/{target.user_id}.jpg",
                    'unreadCount': 0,
                    'index': 3,
                    'lastMessage': {
                        'content': "Last message received",
                        'senderId': 1234,
                        'username': "John Doe",
                        'timestamp': "10:20",
                        'saved': True,
                        'distributed': False,
                        'seen': False,
                        'new': True,
                    },
                    'users': [
                        {
                            '_id': sender.user_id,
                            'username': sender.name,
                            'avatar': f"assets/img/profile/{sender.user_id}.jpg",
                            'status': {
                                'state': "online",
                                'lastChanged': "today, 14:30",
                            },
                        },
                        {
                            '_id': target.user_id,
                            'username': target.name,
                            'avatar': f"assets/img/profile/{target.user_id}.jpg",
                            'status': {
                                'state': "offline",
                                'lastChanged': "14 July, 20:00",
                            },
                        },
                    ],
                    'typingUsers': [target.user_id],
                })

        except Exception as e:
            print(e)

        finally:
            session.close()
            await self.connection.send_text(json.dumps({'rooms': self.rooms}))

    async def get_room_msg(self, con_id):
        try:
            session = Session()
            self.current_room = session.query(CONNECTIONS).filter_by(con_id=con_id).first()

            for msg in self.current_room.messages:
                user = session.query(USERS).filter_by(
                    user_id=msg.sender_id).first()

                self.messages.append({
                    '_id': msg.message_id,
                    'content': msg.content,
                    'senderId': msg.sender_id,
                    'username': user.username,
                    'avatar': f"assets/img/profile/{user.user_id}.jpg",
                    'date': "13 November",
                    'timestamp': "10:20",
                    'system': False,
                    'saved': True,
                    'distributed': True,
                    'seen': True,
                    'disableActions': False,
                    'disableReactions': False,
                    'reactions': {},
                })

        except:
            pass

        finally:
            session.close()
            await self.connection.send_text(json.dumps({'messages': self.messages})) 

    async def send_message(self, message):
        try:
            session = Session()
            new_message = MESSAGES(
                con_id = message['room_id'],
                sender_id = message['sender_id'],
                content = message['content'],
                seen = False
            )

            new_message.update_date()
            session.add(new_message)
            session.commit()

            session.refresh(new_message)
            final_message = json.dumps({
                        'new_message': {
                            '_id': new_message.message_id,
                            'content': new_message.content,
                            'senderId': new_message.sender_id,
                            'username': self.user['username'],
                            'avatar': f"assets/img/profile/{self.user['user_id']}.jpg",
                            'date': "13 November",
                            'timestamp': "10:20",
                            'system': False,
                            'saved': True,
                            'distributed': True,
                            'seen': True,
                            'disableActions': False,
                            'disableReactions': False,
                            'reactions': {},
                        }
                    }
                )

            await self.broadcaster.broadcast_to_user(self.current_room.get_connected_user(new_message.sender_id), final_message)
            await self.connection.send_text(final_message)

        except Exception as e:
            print(e)
            
        finally:
            session.close()


class ChatBroadcaster:
    def __init__(self):
        self.connections: List[Dict(int, WebSocket)] = []

    async def register_connection(self, ws, client_id):
        self.connections.append({client_id: ws})
    
    async def broadcast_to_user(self, user_id, message):
        for con in self.connections:
            if user_id in con:
                await con[user_id].send_text(message)

broadcaster = ChatBroadcaster()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    manager = UserManager()

    await broadcaster.register_connection(websocket, client_id)
    await manager.load_user(websocket, client_id, broadcaster)

    while True:
        data = await manager.connection.receive_text()
        await manager.request_handler(data)
