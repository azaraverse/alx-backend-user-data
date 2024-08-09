#!/usr/bin/env python3
""" New Session Authentication class based on a database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth class
    """

    @staticmethod
    def get_session_from_db(session_id=None):
        """ Simulates database session retrival
        """
        if session_id is None:
            return None

        try:
            session = UserSession.search({"session_id": session_id})[0]
            return session
        except Exception:
            return None

    def create_session(self, user_id: str = None) -> str:
        """ Create a session and store a new UserSession instance
        """
        if not user_id or user_id is None:
            return None

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return user_session.session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve UserID based on a given session_id
        """
        if session_id is None:
            return None

        user_session = self.get_session_from_db(session_id)
        if user_session is None:
            return None

        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        if not created_at:
            return None

        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on session_id from the
        request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        session_linked_user_id = self.user_id_for_session_id(session_id)
        if session_linked_user_id is None:
            return False

        user_session = self.get_session_from_db(session_id)
        if not user_session:
            return False
        user_session.remove()
        return True
