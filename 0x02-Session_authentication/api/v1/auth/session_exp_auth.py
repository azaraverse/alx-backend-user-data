#!/usr/bin/env python3
""" Session Auth - Expiration """
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class
    """
    def __init__(self):
        """ Initialize session duration from environment variable
        """
        duration = os.getenv('SESSION_DURATION', 0)
        try:
            self.session_duration = int(duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Create a session and store the session information
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve User ID based on session ID and expiration logic
        """
        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None

        if self.session_duration <= 0:
            return session_dictionary["user_id"]

        created_at = session_dictionary["created_at"]
        if not created_at:
            return None

        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None
        return session_dictionary["user_id"]
