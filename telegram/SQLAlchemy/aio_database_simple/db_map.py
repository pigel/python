from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Data(Base):
    __tablename__ = 'userdata'
    id = Column(Integer, primary_key=True)
    date = Column(String(255))
    time = Column(String(255))
    chat_id = Column(String(255))
    first_name = Column(String(255))
    username = Column(String(255))
