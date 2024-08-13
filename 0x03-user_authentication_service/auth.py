#!/usr/bin/env python3
""" User Auth Module
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


def _generate_uuid() -> str:
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
    ) -> User:
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

    def get_user_from_session_id(self, session_id: str) -> Union[
        User, None
    ]:
        """ Takes in a single session_id argument, searches for a user
        corresponding to the session_id and returns the user.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Takes in a single user_id argument, performs a search on user
        based on id given and updates the session_id segment of the user
        to None.
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generates a password reset token for an existing user
        """
        if email is None:
            return None

        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a user's password using a generated reset_password
        token that links to the user
        """
        if not reset_token or not password:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                new_password = _hash_password(password)
                self._db.update_user(user.id, hashed_password=new_password)
                self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            raise ValueError
