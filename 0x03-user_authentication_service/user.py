#!/usr/bin/env python3
""" User model module
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """ User model
    Columns:
        id: primary key (int)
        email: non-nullbale string
        hashed_password: non-nullable string
        session_id: nullable string
        reset_token: nullable string
    """

    __tablename__ = "users"

    def __init__(self, *args, **kwargs):
        """ Initializes a User instance
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
