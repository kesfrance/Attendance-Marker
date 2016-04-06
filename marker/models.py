import datetime
from datetime import date
from sqlalchemy import Column, Integer, String, Text, DateTime,\
ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base, engine
from flask.ext.login import UserMixin



class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    #superuser = Column(Boolean, default='False')
    mygroup = relationship("Cell", backref="author")
    
    
class Member(Base):
    __tablename__='cellmember'
    id = Column(Integer, primary_key=True)
    memb_name = Column(String(1024), nullable=False)
    memb_address = Column(String(1024), nullable=True)
    memb_email = Column(String(64), nullable=True)
    memb_contact = Column(String(32), nullable=True)
    memb_foundation = Column(Integer, default=0)
    memb_baptised = Column(Integer, default=0)
    memb_celldate = Column(DateTime, default=date.today())
    memb_wk1 = Column(String(2), default='NM')
    memb_wk2 = Column(String(2), default='NM')
    memb_wk3 = Column(String(2), default='NM')
    memb_wk4 = Column(String(2), default='NM')
    memb_wk5 = Column(String(2), default='NM')
    memb_comment =Column(Text, nullable=True)
    memb_follow = Column(String(1024), default='Undone')
    cell_id = Column(Integer, ForeignKey('cell.id'))

class Cell(Base):
    __tablename__='cell'
    id = Column(Integer, primary_key=True)
    cellname = Column(String(64), nullable=False)
    cellleader = Column(String(1024), nullable=False)
    celldescrip = Column(String(2048), nullable=False, default=' ')
    cellmember = relationship("Member", backref='cellmember') 
    author_id = Column(Integer, ForeignKey('users.id'))
    
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
