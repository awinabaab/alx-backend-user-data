#!/usr/bin/env python3
""" Session Authentication using a DB
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth to handle session authentication mechanism using a DB
    """
    def create_session(self, user_id=None):
        """ Creates a new session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return user_session.session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID bases on @session_id
        """
        if not session_id:
            return None

        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions or len(user_sessions) == 0:
            return None

        user_session = user_sessions[0]

        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroys a UserSession instance
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions or len(user_sessions) == 0:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        UserSession.save_to_file()
        return True
