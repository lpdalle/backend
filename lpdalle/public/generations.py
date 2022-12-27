from flask import Blueprint

from lpdalle.generations.gen_storage import GenerationsStorage
from lpdalle.schemas import Generations

view_user_generations = Blueprint('user_generations', __name__)

storage = GenerationsStorage()


@view_user_generations.get('/<int:user_id>')
def view_generations(user_id: int):
    get_gens = storage.get_user_generations(user_id)
    return [Generations.from_orm(gen).dict() for gen in get_gens]
