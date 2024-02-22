#!/usr/bin/env python3
"""Auth"""
import bcrypt
from db import DB
from user import User

def _hash_password(password: str) -> bytes:
    """_summary_

    Args:
        password (_type_): _description_

    Returns:
        bytes: _description_
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())




class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """_summary_

        Args:
            emal (str): _description_
            password (str): _description_

        Returns:
            User: _description_
        """
        try:
            self._db.find_user_by(email=email)
        except Exception:
            return self._db.add_user(email=email, hashed_password=password)
        raise ValueError("User {} already exists".format(email))