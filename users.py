from dataclasses import dataclass, asdict
from flask import Flask, request
from uuid import uuid4

app = Flask(__name__)

@dataclass
class Users:
    uid: str
    login: str
    email: str

users = []
user1 = Users(uuid4().hex, 'vasya', 'vasya@sobak.net')
user2 = Users(uuid4().hex, 'mafusail', 'mafu@naturlich.net')
users.append(user1)
users.append(user2)


@app.get('/api/v1/users/')
def get_all():
    return users


@app.get('/api/v1/users/<string:uid>')
def get_by_uid(uid: str):
    for user in users:
        if user.uid == uid:
            return asdict(user)
    return 'Такого пользователя нет', 404


@app.post('/api/v1/users/')
def add():
    uid = uuid4().hex
    user = request.json
    user['uid'] = uid
    user_login = request.json["login"]
    user_email = request.json["email"]
    new_user = Users(uid=user['uid'], login=user_login, email=user_email)
    users.append(new_user)
    return user, 201


@app.put('/api/v1/users/<string:uid>')
def update(uid: str):
    update_user = request.json
    for user in users:
        if user.uid == uid:
            user.login = update_user["login"]
            user.email = update_user["email"]
            return asdict(user)
    return 'Такого пользователя нет', 404


@app.delete('/api/v1/users/<string:uid>')
def delete(uid):
    users[:] = [user for user in users if user.uid != uid]
    return [], 204



def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
