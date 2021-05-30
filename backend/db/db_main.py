from sqlalchemy import (
    create_engine,
    Column,
    Table,
    Integer,
    DateTime,
    String,
    ForeignKey,
    Date,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext
from sqlalchemy.sql.sqltypes import Boolean, INTEGER
from datetime import datetime

db_string = "postgresql://postgres:1234@localhost:5432/hokusai" # Conexão com um banco de dados Postgresql
db_engine = create_engine(db_string)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt para fazer a cryptografia da senha

Session = sessionmaker(db_engine)
session = Session()

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
    tags = Column(ARRAY(Integer)) # tags que o user tem interesse

    posts = relationship("POSTS", back_populates="author", lazy='subquery')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password): # Prenche o password_hash automaticamente
        self.password_hash = pwd_context.hash(password)
        
    def verify_password(self, password):
        """
        Verifica se o password e valido
        """
        return pwd_context.verify(password, self.password_hash)
    
    def add_tag(self, session, tag_id):
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
    post_img = Column(ARRAY(String))
    post_type = Column(Integer)
    likes = Column(Integer)
    created_at = Column(DateTime)

    author = relationship("USERS", back_populates="posts", lazy='subquery') # Objeto do sqlalchemy que representa o autor do post
    tags = relationship("TAGS", secondary=posts_tags)

class TAGS(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, unique=True)
    created_at = Column(DateTime)

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
        if self.created_at == None:
            self.created_at = datetime.now()
            
        self.last_updated = datetime.now()

        print(self.last_updated)
    
class CONNECTIONS(Base):
    __tablename__ = "connections"
    con_id = Column(Integer, primary_key=True, autoincrement=True)
    con_status = Column(Boolean) # Se a conexão foi aceita ou recusada
    user_1_id = Column(Integer, ForeignKey('users.user_id')) # O user que pediu a conexão
    user_2_id = Column(Integer, ForeignKey('users.user_id')) # O user que recebeu a requisição de conexão


class NOTIFICATIONS(Base):
    __tablename__ = "NOTIFICATIONS"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    message = Column(String)
    type = Column(Integer) # 0 - Normal, 1 - Conexão
    status = Column(Boolean) 
    created_at = Column(DateTime)


Base.metadata.create_all(db_engine)