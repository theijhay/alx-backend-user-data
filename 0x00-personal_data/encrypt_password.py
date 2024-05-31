#!/usr/bin/env python3
""" Encrypting passwords"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    returns a hashed password
    Arguments:
        password: password to hash
    """
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    returns a boolean
    arguments:
        hashed_password: bytes type
        password: string type
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
