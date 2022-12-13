from dataclasses import asdict
from flask import Flask, request
from storage import UserStorage


app = Flask(__name__)

user_storage = UserStorage()

@app.get('/api/v1/users/')
def get_all():
    users = user_storage.get_all()
    return [asdict(user) for user in users]


@app.get('/api/v1/users/<string:uid>')
def get_by_uid(uid: str):
    if user_storage.get_by_uid(uid):
        return asdict(user_storage.get_by_uid(uid))
    return {}, 404


@app.post('/api/v1/users/')
def add():
    user = request.json
    user_login = request.json["login"]
    user_email = request.json["email"]
    user_storage.add(login=user_login, email=user_email)
    return user, 201


@app.put('/api/v1/users/<string:uid>')
def update(uid: str):
    user_login = request.json["login"]
    user_email = request.json["email"]
    update_user = user_storage.update(uid=uid, login=user_login, email=user_email)
    return asdict(update_user), 201



@app.delete('/api/v1/users/<string:uid>')
def delete(uid):
    if user_storage.delete(uid):
        return {}, 204
    return {}, 404



def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
