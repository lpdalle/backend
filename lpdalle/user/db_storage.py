from sqlalchemy.exc import IntegrityError

from lpdalle.db import db_session
from lpdalle.errors import ConflictError, NotFoundError
from lpdalle.model import User


class UserStorage:
    def get_all(self) -> list[User]:
        return User.query.all()

    def get_by_uid(self, uid: int) -> User | None:
        user = User.query.filter(User.uid == uid).first()
        if not user:
            raise NotFoundError('users', uid)
        return user

    def get_by_login(self, login: str) -> User | None:
        return User.query.filter(User.login == login).first()

    def add(self, login: str, email: str) -> User:
        uid = None
        new_user = User(uid=uid, login=login, email=email)
        db_session.add(new_user)
        db_session.commit()
        return new_user

    def update(self, uid: int, login: str, email: str) -> User:
        user = User.query.filter(User.uid == uid).first()
        if not user:
            raise NotFoundError('users', uid)

        user.login = login
        user.email = email

        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError('users', uid)

        return User.query.filter(User.uid == uid).first()

    def delete(self, uid: int) -> bool:
        user = db_session.query(User).filter(User.uid == uid).first()
        if not user:
            raise NotFoundError('users', uid)

        db_session.delete(user)
        db_session.commit()
        return True
