from flask import Blueprint

from lpdalle.generations.gen_storage import GenerationsStorage
from lpdalle.schemas import Generations

view_generations = Blueprint('generations', __name__)

generations_storage = GenerationsStorage()


@view_generations.get('/<int: uid>')
def get_by_uid(uid: int):
    get_generation = generations_storage.get_by_uid(uid)
    generation = Generations.from_orm(get_generation)
    return generation.dict()
