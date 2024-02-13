#!/usr/bin/env python3
""" Module of auth views
"""
from flask import request


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None or excluded_paths is None:
            return True
        
        if path not in excluded_paths or f'{path}/' not in excluded_paths:
            return True
        
        return False

    def authorization_header(self, request=None) -> str:
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        return None