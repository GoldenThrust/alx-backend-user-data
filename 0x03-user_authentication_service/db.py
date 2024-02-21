"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def user(self, email: str, hashed_password: str):
        """_summary_

        Args:
            email (str): _description_
            hashed_password (str): _description_

        Returns:
            _type_: _description_
        """
        user = None
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()

        return user

    def find_user_by(self, **kwargs):
        """_summary_

        Raises:
            InvalidRequestError: _description_
            NoResultFound: _description_

        Returns:
            _type_: _description_
        """
        users = self._session.query(User)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError

            for user in users:
                if getattr(user, key) == v:
                    return user
        raise NoResultFound
