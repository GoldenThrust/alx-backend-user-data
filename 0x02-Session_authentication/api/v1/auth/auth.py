#!/usr/bin/env python3
""" Authentication Module
"""
from flask import request
from typing import List, TypeVar
from os import getenv

class Auth:
    """Authentication Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication for a given path"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(
                excluded_path.rstrip("*")
            ):
                return False
            elif path == excluded_path or f"{path}/" == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Return authorization header string"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """Current User Interface"""
        return None
    
    def session_cookie(self, request=None):
        """ return session cookie """
        if request is None:
            return None
        
        return request.cookies.get(getenv('SESSION_NAME'))
