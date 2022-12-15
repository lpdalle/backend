from db import engine, Base
from model import User
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select


Session = sessionmaker(bind=engine)
session = Session()
table = Base.metadata.sorted_tables[0] # найти как вытягивать таблицу

# first = User(
#     uid = None,
#     login = 'Stepa',
#     email = 'stepa@mail.ru'
# )

# print(type(first))
# session.add(first)
# session.commit()


# @dataclass
# class User:
#     uid: int #str
#     login: str
#     email: str


class UserStorage:
    # def __init__(self) -> None:
    #     self.storage: dict[str, User] = {}


    def get_all(self) -> list[User]:
        all_users = {}
        for item in session.query(table):
            all_users[item.uid] = {"login": item.login, "email": item.email}
        return list(all_users.values())


    # def get_by_uid(self, uid: str) -> User | None:
    #     user = session.query(table).filter_by(uid=uid).first()
    #     return list(user)

    def get_by_login(self, login: str) -> User | None:
        user = session.query(table).filter_by(login=login).first()
        return list(user)


    def add(self, login: str, email: str) -> User:
        uid = None
        new_user = User(uid=uid, login=login, email=email)
        session.add(new_user)
        session.commit()
        return new_user


    # def update(self, uid: str, login: str, email: str) -> User:
    #     login.email = email
    #     session.commit()
    #     get_by_login(login)
    #     return

    def update(self, login: str, email: str) -> User:
        session.query(table).filter_by(login=login).update({'login': login, 'email':email})
        session.commit()
        user = session.query(table).filter_by(login=login).first()
        return list(user)



    # def delete(self, uid: str) -> bool:
    #     if self.storage.get(uid):
    #         del self.storage[uid]
    #         return True
    #     return False

    def delete(self, login: str) -> bool:
        # user_to_del = session.query(table).filter_by(login=login).first()
        # print(user_to_del)
        if session.query(table).filter_by(login=login).delete(synchronize_session=False):
            return True
        return False

