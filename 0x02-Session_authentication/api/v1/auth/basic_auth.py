#!/usr/bin/env python3
""" Basic Authentication implementation
"""

from api.v1.auth.auth import Auth
from models.user import User
from models.base import Base
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ BasicAuth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Returns the Base64 part of the Authorization header for
        Basic Authentication
        """

        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic"):
            return None

        encoded_auth_header = authorization_header.split(" ")

        return None if len(encoded_auth_header) < 2 else encoded_auth_header[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decodes the value of a Base64 string
        @base64_authorization_header
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf8')
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> str:
        """ Extracts the user email and password from the base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        user_email, user_pwd = decoded_base64_authorization_header.split(":",
                                                                         1)

        return user_email, user_pwd

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> str:
        """ Returns a User instance based on user_email and user_pwd
        """
        if not user_email or not isinstance(user_email, str):
            return None

        if not user_pwd or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users or len(users) == 0:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request
        """
        request_auth_header = self.authorization_header(request)

        encoded_base64_auth_header = self.extract_base64_authorization_header(
                                   request_auth_header)

        decoded_base64_auth_header = self.decode_base64_authorization_header(
                                   encoded_base64_auth_header)

        user_email, user_pwd = self.extract_user_credentials(
                             decoded_base64_auth_header)

        return self.user_object_from_credentials(user_email, user_pwd)
