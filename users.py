from dataclasses import dataclass
from flask import Flask, request
from uuid import uuid4

app = Flask(__name__)

@dataclass
class Users:
    uid: hex
    login: str
    email: str

users = []
user1 = Users(uuid4().hex, 'vasya', 'vasya@sobak.net')
user2 = Users(uuid4().hex, 'mafusail', 'mafu@naturlich.net')
users.append(user1)
users.append(user2)



@app.route('/')
def hello():
    return 'Hello'


@app.get('/api/v1/users/')
def get_all():
    return users


@app.get('/api/v1/users/')
def get_by_uid(uid):
    for user in users:
        if request.json["uid"] == uid:
            return user
    return None


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

@app.put('/api/v1/users/')
def update(uid):
    pass

@app.delete('/api/v1/users/')
def delete(uid):
    pass



def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
