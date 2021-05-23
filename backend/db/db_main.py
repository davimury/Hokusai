from sqlalchemy import (
    create_engine,
    Column,
    Table,
    ARRAY,
    Integer,
    DateTime,
    String,
    ForeignKey,
    Date,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext

db_string = "postgresql://postgres:1234@localhost:5432/hokusai" # Conexão com um banco de dados Postgresql
db_engine = create_engine(db_string)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt para fazer a cryptografia da senha

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

class POSTS(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    post_author = Column(Integer, ForeignKey('users.user_id'))
    post_body = Column(String)
    post_img = Column(ARRAY(String))
    post_reactions = Column(ARRAY(Integer))
    created_at = Column(DateTime)

    author = relationship("USERS", back_populates="posts", lazy='subquery') # Objeto do sqlalchemy que representa o autor do post
    tags = relationship("TAGS", secondary=posts_tags)

class TAGS(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, unique=True)



Base.metadata.create_all(db_engine)