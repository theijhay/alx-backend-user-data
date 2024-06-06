#!/usr/bin/env python3
"""it defines the SessionDBAuth class"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class
    """

    def create_session(self, user_id=None):
        """
        makes the Creator session
        arguments:
           user_id (str): user id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Makes a user ID based on a session ID
        arguments:
            session_id (str): session ID
        returns:
            user ID
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout
        arguments:
            request : request object
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
