#!/usr/bin/env python3
""" Encrypt Password """
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash the provided password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
