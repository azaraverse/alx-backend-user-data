#!/usr/bin/env python3
""" Basic Auth class """
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """ Decodes a base64 authorization header and returns its decoded
        format
        """
        if base64_authorization_header is None or type(
            base64_authorization_header
        ) != str:
            return None
        try:
            base64_decoded = base64.b64decode(base64_authorization_header)
        except BaseException:
            return None
        return base64_decoded.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ Extracts user credentials from an authorization header
        """
        if decoded_base64_authorization_header is None or type(
            decoded_base64_authorization_header
        ) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':'))
