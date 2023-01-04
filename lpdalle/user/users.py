from flask import Blueprint, request

from lpdalle.errors import BadRequestError
from lpdalle.schemas import User
from lpdalle.user.db_storage import UserStorage

view_users = Blueprint('users', __name__)
user_storage = UserStorage()


@view_users.get('/')
def get_all():
    users = user_storage.get_all()
    return [User.from_orm(user).dict() for user in users]


@view_users.get('/<int:uid>')
def get_by_uid(uid: int):
    get_user = user_storage.get_by_uid(uid)
    user = User.from_orm(get_user)
    return user.dict()


@view_users.get('/telegram/<str:telgram_id>')
def get_by_tg_id(telegram_id: str):
    tg_id = user_storage.get_by_telegram_id(telegram_id)
    user = User.from_orm(tg_id)
    return user.dict()


@view_users.post('/')
def add():
    try:
        user = request.json
    except BadRequestError as badrequest_err:
        return badrequest_err

    if not user:
        raise BadRequestError('Empty user data!')

    user['uid'] = -1
    new_user = User(**user)

    new_user_add = user_storage.add(login=new_user.login, email=new_user.email)

    user_add = User.from_orm(new_user_add)
    return user_add.dict(), 201


@view_users.put('/<int:uid>')
def update(uid: int):
    try:
        payload = request.json
    except BadRequestError as badrequest_err:
        return badrequest_err

    if not payload:
        raise BadRequestError('Empty payload')

    payload['uid'] = -1
    user = User(**payload)

    update_user = user_storage.update(
        uid=uid,
        login=user.login,
        email=user.email,
    )

    user = User.from_orm(update_user)
    return user.dict(), 201


@view_users.delete('/<int:uid>')
def delete(uid: int):
    user_storage.delete(uid)
    return {}, 204


