#!/usr/bin/env python3
""" Integration tests """
import requests
from auth import Auth

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Test for registering user"""
    pass


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test for logging in with wrong password """
    pass


def log_in(email: str, password: str) -> str:
    """ Test for logging in with correct password """
    pass


def profile_unlogged() -> None:
    """ Test for profile when not logged in """
    pass


def profile_logged(session_id: str) -> None:
    """Test for profile when not logged in"""
    pass


def log_out(session_id: str) -> None:
    """ Test for logged out """
    pass


def reset_password_token(email: str) -> str:
    """ Test for reset password """
    pass


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test for update password """
    pass


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
