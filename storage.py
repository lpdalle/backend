from dataclasses import dataclass
from uuid import uuid4


@dataclass
class User:
    uid: str
    login: str
    email: str


class UserStorage:
    def __init__(self) -> None:
        self.storage: dict[str, User] = {}


    def get_all(self) -> list[User]:
        return list(self.storage.values())


    def get_by_uid(self, uid: str) -> User | None:
        if self.storage.get(uid):
            return self.storage[uid]


    def add(self, login: str, email: str) -> User:
        uid = uuid4().hex
        new_user = User(uid=uid, login=login, email=email)
        self.storage[new_user.uid] = new_user
        return self.storage[new_user.uid]


    def update(self, uid: str, login: str, email: str) -> User:
        update_user = self.storage[uid]
        update_user.email = email
        update_user.login = login
        return update_user


    def delete(self, uid: str) -> bool:
        if self.storage.get(uid):
            del self.storage[uid]
            return True
        return False

