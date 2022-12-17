from db import db_session
from model import User


class UserStorage:
    def get_all(self) -> list[User]:
        return User.query.all()

    def get_by_uid(self, uid: int) -> User | None:
        return User.query.filter(User.uid == uid).first()

    def get_by_login(self, login: str) -> User | None:
        return User.query.filter(User.login == login).first()

    def add(self, login: str, email: str) -> User:
        uid = None
        new_user = User(uid=uid, login=login, email=email)
        db_session.add(new_user)
        db_session.commit()
        return new_user

    def update(self, uid: int, login: str, email: str) -> User:
        db_session.query(User).filter(User.uid == uid).update({
            'login': login,
            'email': email,
        })
        db_session.commit()
        return User.query.filter(User.uid == uid).first()

    def delete(self, uid: int) -> bool:
        user = db_session.query(User).filter(User.uid == uid)
        if not user:
            return False

        user.delete(synchronize_session=False)
        db_session.commit()
        return True
