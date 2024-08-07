#!/usr/bin/env python3
""" API Basic Authentication """
from flask import request
from typing import List, TypeVar


class Auth:
    """"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth public method instance
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization header public method instance
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user public method instance
        """
        return None
