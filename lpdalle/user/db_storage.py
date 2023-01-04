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
            raise NotFoundError('users', str(uid))
        return user

    def get_by_login(self, login: str) -> User | None:
        user = User.query.filter(User.login == login).first()
        if not user:
            raise NotFoundError('users', login)
        return user

    def get_by_telegram_id(self, telegram_id: str):
        user = db_session.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            raise NotFoundError('users', telegram_id)
        return user

    def add(self, login: str, email: str) -> User:
        new_user = User(login=login, email=email)
        db_session.add(new_user)

        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError('users', new_user.uid)

        return new_user

    def update(self, uid: int, login: str, email: str) -> User:
        user = User.query.filter(User.uid == uid).first()
        if not user:
            raise NotFoundError('users', str(uid))

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
            raise NotFoundError('users', str(uid))

        db_session.delete(user)
        db_session.commit()
        return True
