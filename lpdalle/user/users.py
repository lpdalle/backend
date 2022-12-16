from flask import request
from flask import Blueprint
from lpdalle.user.db_storage import UserStorage



users_view = Blueprint('users', __name__)
user_storage = UserStorage()


@users_view.get('/')
def get_all():
    users = user_storage.get_all()
    all_users = []
    for user in users:
        all_users.append({'uid': user.uid, 'login': user.login, 'email': user.email})
    return all_users


@users_view.get('/<string:login>')
def get_by_login(login: str):
    user = user_storage.get_by_login(login)
    if user:
        return {'uid': user.uid, 'login': user.login, 'email': user.email}
    return {}, 404


@users_view.post('/')
def add():
    user = request.json
    user_login = request.json["login"]
    user_email = request.json["email"]
    user_storage.add(login=user_login, email=user_email)
    return user, 201


@users_view.put('/<string:login>')
def update(login: str):
    user_login = request.json["login"]
    user_email = request.json["email"]
    update_user = user_storage.update(login=user_login, email=user_email)
    if update_user:
        return {'uid': update_user.uid, 'login': update_user.login, 'email': update_user.email}, 200
    return {}, 404


@users_view.delete('/<string:login>')
def delete(login):
    if user_storage.delete(login):
        return {}, 204
    return {}, 404


