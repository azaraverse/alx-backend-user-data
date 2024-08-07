#!/usr/bin/env python3
""" API Basic Authentication """
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth public method instance
        """
        if not excluded_paths:
            return True

        if path and not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # check if the excluded paths end with *
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header public method instance
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user public method instance
        """
        return None
