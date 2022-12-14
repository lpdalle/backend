from dataclasses import asdict
from flask import request
from flask import Blueprint
from lpdalle.user.storage import UserStorage


users_view = Blueprint('users', __name__)

user_storage = UserStorage()

@users_view.get('/')
def get_all():
    users = user_storage.get_all()
    return [asdict(user) for user in users]


@users_view.get('/<string:uid>')
def get_by_uid(uid: str):
    if user_storage.get_by_uid(uid):
        return asdict(user_storage.get_by_uid(uid))
    return {}, 404


@users_view.post('/')
def add():
    user = request.json
    user_login = request.json["login"]
    user_email = request.json["email"]
    user_storage.add(login=user_login, email=user_email)
    return user, 201


@users_view.put('/<string:uid>')
def update(uid: str):
    user_login = request.json["login"]
    user_email = request.json["email"]
    update_user = user_storage.update(uid=uid, login=user_login, email=user_email)
    return asdict(update_user), 200


@users_view.delete('/<string:uid>')
def delete(uid):
    if user_storage.delete(uid):
        return {}, 204
    return {}, 404


