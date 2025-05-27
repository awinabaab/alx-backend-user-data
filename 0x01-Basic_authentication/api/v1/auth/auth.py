#!/usr/bin/env python3
""" A class to manage API authentication
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication implementation
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if @path requires authentication
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        for ex_path in excluded_paths:
            if not ex_path:
                continue

            if ex_path.endswith("*"):
                if path.startswith(ex_path[:-1]):
                    return False
            else:
                if not ex_path.endswith("/"):
                    ex_path += "/"
                if path == ex_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header in the request headers
        """
        if request is None or "Authorization" not in request.headers.keys():
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user object
        """
        return None
