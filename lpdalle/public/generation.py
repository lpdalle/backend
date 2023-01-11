from flask import Blueprint

from lpdalle.generation.storage import GenerationStorage
from lpdalle.schemas import Generation

view_user_generations = Blueprint('user_generation', __name__)

storage = GenerationStorage()


@view_user_generations.get('/<int:user_id>')
def view_generations(user_id: int):
    get_gens = storage.get_user_generations(user_id)
    return [Generation.from_orm(gen).dict() for gen in get_gens]
