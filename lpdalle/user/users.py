from flask import Blueprint, request

from lpdalle.user.db_storage import UserStorage

users_view = Blueprint('users', __name__)
user_storage = UserStorage()


@users_view.get('/')
def get_all():
    users = user_storage.get_all()
    all_users = []
    for user in users:
        all_users.append({
            'uid': user.uid,
            'login': user.login,
            'email': user.email,
        })
    return all_users


@users_view.get('/<int:uid>')
def get_by_uid(uid: int):
    user = user_storage.get_by_uid(uid)
    if user:
        return {'uid': user.uid, 'login': user.login, 'email': user.email}
    return {}, 404


@users_view.post('/')
def add():
    user = request.json
    if not user:
        return {}, 400

    user_login = user['login']
    user_email = user['email']
    user_storage.add(login=user_login, email=user_email)
    return user, 201


@users_view.put('/<int:uid>')
def update(uid: int):
    payload = request.json
    if not payload:
        return {}, 400

    user_login = payload['login']
    user_email = payload['email']
    update_user = user_storage.update(
        uid=uid,
        login=user_login,
        email=user_email,
    )

    if not update_user:
        return {}, 404

    return {
        'uid': update_user.uid,
        'login': update_user.login,
        'email': update_user.email,
    }, 200


@users_view.delete('/<int:uid>')
def delete(uid: int):
    if user_storage.delete(uid):
        return {}, 204
    return {}, 404
