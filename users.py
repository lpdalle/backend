from flask import Flask, request
from storage import UserStorage
from uuid import uuid4

app = Flask(__name__)

users = UserStorage()

@app.get('/api/v1/users/')
def get_all():
    return users.get_all()


@app.get('/api/v1/users/<string:uid>')
def get_by_uid(uid: str):
    if users.get_by_uid(uid):
        return users.get_by_uid(uid)
    return {}, 404


@app.post('/api/v1/users/')
def add():
    user = request.json
    user_login = request.json["login"]
    user_email = request.json["email"]
    users.add(login=user_login, email=user_email)
    return user, 201


@app.put('/api/v1/users/<string:uid>')
def update(uid: str):
    user_login = request.json["login"]
    user_email = request.json["email"]
    users.update(uid=uid, login=user_login, email=user_email)
    return users.get_by_uid(uid), 201


@app.delete('/api/v1/users/<string:uid>')
def delete(uid):
    if users.get_by_uid(uid):
        users.delete(uid)
        return {}, 204
    return {}, 404



def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
