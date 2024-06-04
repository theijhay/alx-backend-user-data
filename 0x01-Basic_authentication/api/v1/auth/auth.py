#!/usr/bin/env python3
"""
Class AUTH
"""
from flask import request
from typing import (
    List,
    TypeVar
)
User = TypeVar('User')


class Auth:
    """
    Incapsulates the authentication logic
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a provided path necessitates authentication.
        Args:
            - path (str): The URL path to evaluate.
            - excluded_paths (List of str): Paths exempted from authentication.
        Return:
            - True if the path is not in excluded_paths; else False."""
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for a in excluded_paths:
                if a.startswith(path):
                    return False
                if path.startswith(a):
                    return False
                if a[-1] == "*":
                    if path.startswith(a[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the value of the Authorization header in the request
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> User:
        """
        Returns None: just a placeholder
        """
        return None