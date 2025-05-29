#!/usr/bin/env python3
""" User Session Authentication
"""

from models.base import Base
from uuid import uuid4


class UserSession(Base):
    """ User session athentication model
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id', str(uuid4()))
