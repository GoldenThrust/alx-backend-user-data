#!/usr/bin/env python3
""" Session Database Authentication
"""
import uuid
from models.user import User
from api.v1.auth.auth import Auth
from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """session database authentication"""

    def create_session(self, user_id=None):
        """creates a session"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession()
        user_session.user_id = user_id
        user_session.session_id = session_id
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user id for a given session id."""
        if session_id is None or not isinstance(session_id, str):
            return None

        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None

        user = user_session[0]

        if self.session_duration <= 0:
            return user.get("user_id")

        expiration_time = user.get("created_at") + timedelta(
            seconds=self.session_duration
        )
        if expiration_time < datetime.now():
            return None
        return user.get("user_id")

    def destroy_session(self, request=None):
        """destroy the session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session[0].remove()
        return True
