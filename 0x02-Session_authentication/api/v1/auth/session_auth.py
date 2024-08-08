#!/usr/bin/env python3
""" Session Auth Class """
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session id for a given user id
        """
        if user_id is None or type(user_id) != str:
            return None
        self.session_id = str(uuid4())
        self.user_id_by_session_id[self.session_id] = user_id
        return self.session_id
