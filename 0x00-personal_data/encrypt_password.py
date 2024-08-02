#!/usr/bin/env python3
""" Encrypting Passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """ A function that hashes and encrypts a password

    Args:
        password: A string representing user password
    Returns:
        A byte string
    """
    pwd = password.encode("utf-8")
    return bcrypt.hashpw(pwd, bcrypt.gensalt())
