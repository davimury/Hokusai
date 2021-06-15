from sqlalchemy import (
    create_engine,
    Column,
    Table,
    Integer,
    DateTime,
    String,
    ForeignKey,
    event
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.sqltypes import Boolean, JSON
from passlib.context import CryptContext
from datetime import datetime

# Conexão com um banco de dados Postgresql
db_string = "postgresql://postgres:1234@127.0.0.1:5432/hokusai"
db_engine = create_engine(db_string)

# bcrypt para fazer a cryptografia da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Session = sessionmaker(db_engine)

Base = declarative_base()

posts_tags = Table('posts_tags', Base.metadata,
                   Column('post_id', Integer, ForeignKey('posts.post_id')),
                   Column('tag_id', Integer, ForeignKey('tags.tag_id'))
                   )


class USERS(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    tags = Column(ARRAY(Integer))  # tags que o user tem interesse

    posts = relationship("POSTS", back_populates="author", lazy='joined')
    messages = relationship("MESSAGES", back_populates="user", lazy='joined')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):  # Prenche o password_hash automaticamente
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):  # Verifica se o password e valido
        return pwd_context.verify(password, self.password_hash)

    def add_tag(self, session, tag_id):  # Adiciona uma tag a coluna Tags:List
        if self.tags is not None:
            tags_arr = self.tags
        else:
            tags_arr = []

        self.tags = None
        session.commit()
        session.refresh(self)

        tags_arr.append(tag_id)
        self.tags = tags_arr
        session.commit()


class POSTS(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    post_author = Column(Integer, ForeignKey('users.user_id'))
    post_body = Column(String)
    post_desc = Column(String)
    post_img = Column(ARRAY(String))
    post_type = Column(Integer)
    likes = Column(Integer)
    created_at = Column(DateTime)

    # Objeto do sqlalchemy que representa o autor do post
    author = relationship("USERS", back_populates="posts", lazy='joined')
    tags = relationship("TAGS", secondary=posts_tags)


class TAGS(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, unique=True)
    created_at = Column(DateTime)

    posts = relationship("POSTS", secondary=posts_tags, viewonly=True)

    def update_date(self):
        self.created_at = datetime.now() if self.created_at == None else None


class LIKES(Base):
    __tablename__ = "likes"
    like_id = Column(Integer, primary_key=True, autoincrement=True)
    like_type = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    created_at = Column(DateTime)
    last_updated = Column(DateTime)

    user = relationship("USERS")
    post = relationship("POSTS")

    def update_date(self):
        self.created_at = datetime.now() if self.created_at == None else None
        self.last_updated = datetime.now()


class CONNECTIONS(Base):
    __tablename__ = "connections"
    con_id = Column(Integer, primary_key=True, autoincrement=True)
    con_status = Column(Boolean)  # Se a conexão foi aceita ou recusada
    
    # O user que pediu a conexão
    user_1_id = Column(Integer, ForeignKey('users.user_id'))
    # O user que recebeu a requisição de conexão
    user_2_id = Column(Integer, ForeignKey('users.user_id'))

    messages = relationship("MESSAGES", lazy='joined')

    def in_con(self, user_id):
        if user_id == self.user_1_id:
            return True
        elif user_id == self.user_2_id:
            return True
        else:
            return False

    def get_connected_user(self, user_id):
        if user_id == self.user_1_id:
            return self.user_2_id
        elif user_id == self.user_2_id:
            return self.user_1_id
        else:
            return None


class NOTIFICATIONS(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_id = Column(Integer, ForeignKey('users.user_id'))
    recipient_id = Column(Integer, ForeignKey('users.user_id'))
    con_id =  Column(Integer, ForeignKey('connections.con_id',  ondelete='CASCADE'))
    type = Column(Integer)  # 0 - Mensagem, 1 - Conexão recebida, 2 - Conexão efetuada
    content = Column(JSON)
    status = Column(Boolean)
    created_at = Column(DateTime)
    last_updated = Column(DateTime)

    def update_date(self):
        self.created_at = datetime.now() if self.created_at == None else None
        self.last_updated = datetime.now()

class MESSAGES(Base):
    __tablename__ = "messages"
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    con_id = Column(Integer, ForeignKey('connections.con_id'))
    sender_id = Column(Integer, ForeignKey('users.user_id'))
    reply_id = Column(Integer)
    content = Column(String)
    created_at = Column(DateTime)
    seen = Column(Boolean)
    
    user = relationship("USERS", back_populates="messages", lazy='joined')

    def update_date(self):
        self.created_at = datetime.now() if self.created_at == None else None
        self.last_updated = datetime.now()

    def seen_message(self):
        self.seen = True



Base.metadata.create_all(db_engine)
