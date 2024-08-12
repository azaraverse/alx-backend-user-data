#!/usr/bin/env python3
""" DB module
"""
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """ DB class
    """
    def __init__(self) -> None:
        """ Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add and save a user to the database

        Args:
            email: User email
            password: User password

        Returns:
            User object on success
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Takes in arbitrary keywords and returns the first row found in
        the users table, filtered by this method's input arguments
        """
        try:
            user = self._session.query(User)
            filtered_user = user.filter_by(**kwargs).one()
            return filtered_user
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user object based on user_id and field to update
        """
        user_to_update = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user_to_update, key):
                raise ValueError
            setattr(user_to_update, key, value)
        self._session.commit()
