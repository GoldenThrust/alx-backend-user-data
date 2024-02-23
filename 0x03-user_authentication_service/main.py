#!/usr/bin/env python3
""" Integration tests """
import requests
from auth import Auth

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def base_url(request_uri):
    return f"http://0.0.0.0:5000{request_uri}"


def register_user(email: str, password: str) -> None:
    """ Test for registering user"""
    url = base_url("/users")
    data = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test for logging in with wrong password """
    url = base_url("/sessions")
    data = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Test for logging in with correct password """
    url = base_url("/sessions")
    data = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """ Test for profile when not logged in """
    url = base_url("/profile")
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test for profile when not logged in"""
    url = base_url("/profile")
    cookies = {
        'session_id': session_id,
    }
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """ Test for logged out """
    url = base_url("/sessions")
    cookies = {
        'session_id': session_id,
    }
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ Test for responseet password """
    url = base_url("/reset_password")
    data = {
        'email': email,
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    reset_token = response.cookies.get('reset_token')
    assert response.json() == {"email": email, "reset_token": reset_token}
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test for update password """
    url = base_url("/reset_password")
    data = {
        'email': email,
        'reset_token': responseet_token,
        'new_password': new_password,
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


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
