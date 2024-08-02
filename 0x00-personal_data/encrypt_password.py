#!/usr/bin/env python3
""" Encrypting Passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """ A function that hashes and encrypts a password

    Args:
        password: a string representing user password
    Returns:
        A byte string
    """
    pwd = password.encode("utf-8")
    return bcrypt.hashpw(pwd, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ A function that validates that a password matches a
    corresponding hashed password

    Args:
        hashed_password: encrypted password in bytes
        password: password string literal
    Returns:
        Boolean
    """
    pwd = password.encode("utf-8")
    return bcrypt.checkpw(pwd, hashed_password)
