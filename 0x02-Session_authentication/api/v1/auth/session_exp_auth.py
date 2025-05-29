#!/usr/bin/env python3
""" Session Authentication with an expiry date
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class
    """
    user_id_by_session_id = {}

    def __init__(self):
        """ Instantiate an object
        """
        SESSION_DURATION = os.getenv("SESSION_DURATION")

        try:
            self.session_duration = int(SESSION_DURATION)
        except ValueError as v:
            seslf.session_duration = 0

    def create_session(self, user_id=None):
        """ Creates a session with and expiry date
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {
                              "user_id": user_id,
                              "created_at": datetime.now()
                              }

        SessionExpAuth.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieves a User ID based on @session_id
        """
        if not session_id:
            return None

        session_dict = SessionExpAuth.user_id_by_session_id.get(session_id)

        if not session_dict:
            return None

        user_id = session_dict.get("user_id")
        created_at = session_dict.get("created_at")

        if self.session_duration <= 0:
            return user_id

        if not created_at:
            return None

        expires_at = created_at + timedelta(seconds=self.session_duration)
        if expires_at < datetime.now():
            return None

        return user_id
