from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer ,primary_key = True )
    original = Column(String)
    short_url = Column(String, unique = True)
    create_time = Column(DateTime)

class Click_count(Base):
    __tablename__ = "clicks"

    id = Column(Integer,primary_key = True)
    url_id = Column(Integer)
    ip_add = Column(String)
    user_agent = Column(String)
    clicktime = Column(DateTime)


