from dataclasses import dataclass, asdict
from uuid import uuid4


@dataclass
class Users:
    uid: str
    login: str
    email: str


class UserStorage:
    def __init__(self) -> None:
        self.storage: dict[str, dict[str]] = {}


    def get_all(self) -> list[dict[str]]:
        return list(self.storage.values())


    def get_by_uid(self, uid: str) -> dict:
        if self.storage.get(uid):
            return asdict(self.storage[uid])


    def add(self, login: str, email: str) -> dict:
        uid = uuid4().hex
        new_user = Users(uid=uid, login=login, email=email)
        self.storage[new_user.uid] = new_user
        return self.storage[new_user.uid]


    def update(self, uid: str, login: str, email: str) -> dict:
        self.storage[uid] = Users(uid=uid, login=login, email=email)
        return self.storage[uid]


    def delete(self, uid: str):
        if self.storage.get(uid):
            del self.storage[uid]
        return


