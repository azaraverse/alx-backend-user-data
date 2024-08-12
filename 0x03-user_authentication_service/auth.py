#!/usr/bin/env python3
""" User Auth
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ Hashes user password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def _generate_uuid():
    """ Generates a random uuid and returns it
    """
    return str(uuid4())


class Auth:
    """ Auth class to interact with the authentication database
    """
    def __init__(self) -> None:
        """ Initialize the Auth class
        """
        self._db = DB()

    def register_user(
            self, email: str, password: str
    ) -> Union[None, User]:
        """ A method that registers a new user and hashes the new user's
        password
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password
            )
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if user login is a valid login
        """
        try:
            user = self._db.find_user_by(email=email)
            encoded_pwd = password.encode("utf-8")
            if user and bcrypt.checkpw(encoded_pwd, user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """ Creates a session ID for a given user email if the email
        exists in the database.

        Returns:
            Generated session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None
