#!/usr/bin/env python3
""" Basic Auth class """
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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
            return base64_decoded.decode('utf-8')
        except Exception:
            return None

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

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ Extracts user obj from given credentials and returns the
        User object
        """
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if not users:
            return None

        user = users[0]
        if not User.is_valid_password(user, user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth() and retrieves User instance for a
        request
        """
        header = self.authorization_header(request)
        if not header:
            return None

        base64_header = self.extract_base64_authorization_header(header)
        if not base64_header:
            return None

        decode_base64 = self.decode_base64_authorization_header(
            base64_header
        )
        if not decode_base64:
            return None

        credentials = self.extract_user_credentials(decode_base64)
        if credentials[0] is None or credentials[1] is None:
            return None

        return self.user_object_from_credentials(
            credentials[0], credentials[1]
        )
