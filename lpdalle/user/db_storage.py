from db import engine
from model import User
from sqlalchemy.orm import Session, sessionmaker


Session = sessionmaker(bind=engine)
session = Session()


class UserStorage:
    def get_all(self) -> list[User]:
        all_users = User.query.all()
        users = []
        for user in all_users:
            users.append({'uid': user.uid, 'login': user.login, 'email': user.email})
        return users


    def get_by_login(self, login: str) -> User | None:
        user = User.query.filter(User.login == login).first()
        return {'uid': user.uid, 'login': user.login, 'email': user.email}


    def add(self, login: str, email: str) -> User:
        uid = None
        new_user = User(uid=uid, login=login, email=email)
        session.add(new_user)
        session.commit()
        return new_user


    def update(self, login: str, email: str) -> User:
        session.query(User).filter(User.login == login).update({'login': login, 'email':email})
        session.commit()
        user = User.query.filter(User.login==login).first()
        return {'uid': user.uid, 'login': user.login, 'email': user.email}


    def delete(self, login: str) -> bool:
        if session.query(User).filter(User.login==login).delete(synchronize_session=False):
            session.commit()
            return True
        return False

