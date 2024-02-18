#!/usr/bin/env python3
""" Session expiration Authentication
"""
import uuid
from os import getenv
from models.user import User
from api.v1.auth.auth import Auth
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """session authentication with expirations."""

    def __init__(self):
        """initialize a new session"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a session"""
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        session_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user id for a given session id."""

        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        created_at = session_dict.get("created_at")
        if not created_at:
            return None
        
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        

        exp_time =  created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None
        
        return session_dict.get('user_id')
