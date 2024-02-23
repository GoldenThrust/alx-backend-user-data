#!/usr/bin/env python3
"""Authentication provider"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from typing import Optional
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """_summary_

    Args:
        password (_type_): _description_

    Returns:
        bytes: _description_
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

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

            return self._db.add_user(
                email=email, hashed_password=_hash_password(password)
            )
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            bool: _description_
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email: str) -> str:
        """_summary_

        Args:
            email (str): _description_

        Returns:
            str: _description_
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """_summary_

        Args:
            session_id (str): _description_

        Returns:
            Optional[User]: _description_
        """
        if session_id is None:
            return None

        user = None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            pass

        return user

    def destroy_session(self, user_id: int) -> None:
        """_summary_

        Args:
            user_id (int): _description_
        """
        try:
            user = self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

        return None

    def get_reset_password_token(self, email: str) -> str:
        """_summary_

        Args:
            email (str): _description_
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """_summary_

        Args:
            reset_token (str): _description_
            password (str): _description_

        Raises:
            ValueError: _description_
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed_password = _hash_password(password)

        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None,
        )
