from flask import Blueprint
from lpdalle.user.db_storage import UserStorage


view_login = Blueprint('user_login', __name__)

user_storage = UserStorage()


@view_login.get('/<string:login>')
def get_by_login(login: str):
    user = user_storage.get_by_login(login)
    if user:
        return {'uid': user.uid, 'login': user.login, 'email': user.email}
    return {}, 404
