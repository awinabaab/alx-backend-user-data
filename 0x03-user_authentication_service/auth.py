#!/usr/bin/env python3
""" Auth module
"""

import bcrypt
from db import DB
from user import User
from typing import TypeVar
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """ Auth services for User
    """

    def __init__(self):
        """ Initializes an Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """ Registers a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            password_hash = _hash_password(password)
            new_user = self._db.add_user(email, password_hash)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if the email-password pair are compatible
        """
        try:
            user = self._db.find_user_by(email=email)
            password_bytes = password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, user.hashed_password)
        except Exception as e:
            pass

        return False

    def create_session(self, email: str) -> str:
        """ Generates and returns a session_id as a string
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Returns a User corresponding to @session_id
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception as e:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ Destroys a session corresponding to a User
        """
        if user_id is None:
            return None

        try:
            return self._db.update_user(user_id, session_id=None)
        except ValueError as e:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generates a returns a reset_token for a using correspondin to email
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception as e:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates the password of a user corresponding to @reset_token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            password_hash = _hash_password(password)
            return self._db.update_user(user.id,
                                        hashed_password=password_hash,
                                        reset_token=None
                                        )
        except Exception as e:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """ Hashes a password string and returns bytes
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)

    return password_hash


def _generate_uuid() -> str:
    """ Generates and returns a string representation of a uuid
    """
    return str(uuid4())
