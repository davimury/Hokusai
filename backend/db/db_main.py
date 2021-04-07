from datetime import date, datetime
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
from sqlalchemy.orm import sessionmaker, relationship, backref
from dateutil.relativedelta import relativedelta
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union

db_string = "postgresql://postgres:1234@localhost:5432/tcc" # Conexão com um banco de dados Postgresql

db = create_engine(db_string)
Session = sessionmaker(db)

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt para fazer a cryptografia da senha

class USERS(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
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
    
class V_USERS(BaseModel):
    email: str
    password: str
    
    
class POSTS(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    post_body = Column(String)
    created_at = Column(DateTime)

class V_POSTS(BaseModel):
    post_body: str
    
    
class TAGS(base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, unique=True)

class V_TAGS(BaseModel):
    tag_name: str

base.metadata.create_all(db)