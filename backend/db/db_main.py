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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

db_string = "postgresql://postgres:root@localhost:5432/tcc" # Conexão com um banco de dados Postgresql
db_engine = create_engine(db_string)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt para fazer a cryptografia da senha

Session = sessionmaker(db_engine)
Base = declarative_base()

class USERS(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    
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
    post_body = Column(String)
    created_at = Column(DateTime)

class TAGS(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, unique=True)


Base.metadata.create_all(db_engine)