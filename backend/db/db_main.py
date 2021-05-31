from sqlalchemy import (
    create_engine,
    Column,
    Table,
    Integer,
    DateTime,
    String,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.sqltypes import Boolean
from passlib.context import CryptContext
from datetime import datetime

# Conexão com um banco de dados Postgresql
db_string = "postgresql://postgres:1234@127.0.0.1:5432/hokusai"
db_engine = create_engine(db_string)

# bcrypt para fazer a cryptografia da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    tags = Column(ARRAY(Integer))  # tags que o user tem interesse

    posts = relationship("POSTS", back_populates="author", lazy='subquery')

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
    post_img = Column(ARRAY(String))
    post_type = Column(Integer)
    likes = Column(Integer)
    created_at = Column(DateTime)

    # Objeto do sqlalchemy que representa o autor do post
    author = relationship("USERS", back_populates="posts", lazy='subquery')
    tags = relationship("TAGS", secondary=posts_tags)


class TAGS(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, unique=True)
    created_at = Column(DateTime)

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
    """ __table_args__ = (UniqueConstraint('user_1_id', 'user_2_id'),) """
    con_id = Column(Integer, primary_key=True, autoincrement=True)
    con_status = Column(Boolean)  # Se a conexão foi aceita ou recusada

    # O user que pediu a conexão
    user_1_id = Column(Integer, ForeignKey('users.user_id'))
    # O user que recebeu a requisição de conexão
    user_2_id = Column(Integer, ForeignKey('users.user_id'))


class NOTIFICATIONS(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_id = Column(Integer, ForeignKey('users.user_id'))
    recipient_id = Column(Integer, ForeignKey('users.user_id'))
    con_id =  Column(Integer, ForeignKey('connections.con_id'))
    type = Column(Integer)  # 0 - Normal, 1 - Conexão
    status = Column(Boolean)
    created_at = Column(DateTime)
    last_updated = Column(DateTime)

    def update_date(self):
        self.created_at = datetime.now() if self.created_at == None else None
        self.last_updated = datetime.now()


Base.metadata.create_all(db_engine)
