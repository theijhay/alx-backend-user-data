#!/usr/bin/env python3
"""
DB Module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """Class for database operations
    """

    def __init__(self) -> None:
        """Constructor for DB class
        """
        self._engine = create_engine("sqlite:///a.db",
                                     echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Property for session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database
        Args:
            email (str): The email of the user
            hashed_password (str): The hashed password of the user
        Return:
            The newly created User object
        """
        user_instance = User(email=email, hashed_password=hashed_password)
        self._session.add(user_instance)
        self._session.commit()
        return user_instance

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by matching attributes
        Args:
            attributes (dict): The attributes to match the user
        Return:
            The matching user or an error
        """
        all_users = self._session.query(User)
        for attribute, value in kwargs.items():
            if attribute not in User.__dict__:
                raise InvalidRequestError
            for user in all_users:
                if getattr(user, attribute) == value:
                    return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates the attributes of a user
        Args:
            user_id (int): The id of the user
            kwargs (dict): The attributes to update and their new values
        Return:
            None
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for attribute, value in kwargs.items():
            if hasattr(user, attribute):
                setattr(user, attribute, value)
            else:
                raise ValueError
        self._session.commit()
