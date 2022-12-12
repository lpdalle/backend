from dataclasses import dataclass, asdict
from flask import Flask, request
from uuid import uuid4

app = Flask(__name__)

@dataclass
class Users:
    uid: str
    login: str
    email: str

users = {}


@app.get('/api/v1/users/')
def get_all():
    return list(users.values())


@app.get('/api/v1/users/<string:uid>')
def get_by_uid(uid: str):
    if users.get(uid):
        return asdict(users[uid])
    return {}, 404


@app.post('/api/v1/users/')
def add():
    uid = uuid4().hex
    user = request.json
    user['uid'] = uid
    user_login = request.json["login"]
    user_email = request.json["email"]
    new_user = Users(uid=user['uid'], login=user_login, email=user_email)
    users[new_user.uid] = new_user
    return user, 201


@app.put('/api/v1/users/<string:uid>')
def update(uid: str):
    user_login = request.json["login"]
    user_email = request.json["email"]
    users[uid] = Users(uid=uid, login=user_login, email=user_email)
    return asdict(users[uid]), 201


@app.delete('/api/v1/users/<string:uid>')
def delete(uid):
    if users.get(uid):
        del users[uid]
        return {}, 204
    return {}, 404



def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
