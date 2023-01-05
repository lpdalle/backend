from flask import Blueprint

from lpdalle.schemas import User
from lpdalle.user.db_storage import UserStorage

view_login = Blueprint('login', __name__)
user_storage = UserStorage()


@view_login.get('/<string:login>')
def get_by_login(login: str):
    get_user = user_storage.get_by_login(login)
    user = User.from_orm(get_user)
    return user.dict()
