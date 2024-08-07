#!/usr/bin/env python3
""" Basic Auth class """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Authenticator class that inherits from Auth()
    """
    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """ Extracts base64 authorization header and returns the value
        after the Basic keyword
        """
        if authorization_header is None or type(authorization_header) != str:  # nopep8
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]
