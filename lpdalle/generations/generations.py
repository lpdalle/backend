from flask import Blueprint, request

from lpdalle.errors import BadRequestError
from lpdalle.generations.gen_storage import GenerationsStorage
from lpdalle.schemas import Generations

view_generations = Blueprint('generations', __name__)

generations_storage = GenerationsStorage()


@view_generations.get('/<int:uid>')
def get_by_uid(uid: int):
    get_generation = generations_storage.get_by_uid(uid)
    generation = Generations.from_orm(get_generation)
    return generation.dict()

# TODO: add user all generations
# @view_generations.get('/<int:user_id>')
# def get_user_generations(user_id: int):
#     pass


@view_generations.post('/')
def add():
    try:
        generation = request.json
    except BadRequestError as badrequest_err:
        return {'message': badrequest_err}

    if not generation:
        raise BadRequestError('Empty generation data!')

    generation['uid'] = -1
    new_generation = Generations(**generation)

    generation_add = generations_storage.add(
        user_id=new_generation.user_id,
        prompt=new_generation.prompt,
        status=new_generation.status,
    )

    new_gen_add = Generations.from_orm(generation_add)
    return new_gen_add.dict(), 201
