from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from lpdalle.errors import BadRequestError, ConflictError
from lpdalle.generations.gen_storage import GenerationsStorage
from lpdalle.schemas import Generations

view_generations = Blueprint('generations', __name__)

generations_storage = GenerationsStorage()


@view_generations.get('/<int:uid>')
def get_by_uid(uid: int):
    get_generation = generations_storage.get_by_uid(uid)
    generation = Generations.from_orm(get_generation)
    return generation.dict()


@view_generations.post('/')
def add():
    try:
        generation = request.json
    except BadRequestError:
        raise BadRequestError('message')

    if not generation:
        raise BadRequestError('Empty generation data!')

    generation['uid'] = -1
    new_generation = Generations(**generation)

    try:
        generation_add = generations_storage.add(
            user_id=new_generation.user_id,
            prompt=new_generation.prompt,
            status=new_generation.status,
        )
    except IntegrityError:
        raise ConflictError('generations', new_generation.uid)
    new_gen_add = Generations.from_orm(generation_add)
    return new_gen_add.dict(), 201
