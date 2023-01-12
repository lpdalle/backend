from flask import Blueprint, request

from lpdalle.errors import BadRequestError
from lpdalle.generation.storage import GenerationStorage
from lpdalle.schemas import Generation

view_generation = Blueprint('generation', __name__)
view_user_generations = Blueprint('user_generations', __name__)
storage = GenerationStorage()


@view_generation.get('/<int:uid>')
def get_by_uid(uid: int):
    get_generation = storage.get_by_uid(uid)
    generation = Generation.from_orm(get_generation)
    return generation.dict()


@view_user_generations.get('/')
def get_by_user_id(user_id: int):
    get_generation = storage.get_user_generations(user_id)
    return [Generation.from_orm(generation).dict() for generation in get_generation]


@view_user_generations.post('/')
def add(user_id: int):
    try:
        payload = request.json
    except BadRequestError as badrequest_err:
        return {'Empty data!': badrequest_err}

    if not payload:
        raise BadRequestError('Empty generation data!')

    payload['uid'] = -1
    payload['user_id'] = user_id
    generation = Generation(**payload)

    new_generation = storage.add(
        user_id=generation.user_id,
        prompt=generation.prompt,
        status=generation.status,
    )

    new_gen_add = Generation.from_orm(new_generation)
    return new_gen_add.dict(), 201


@view_generation.put('/acquire')
def update_status():
    update = storage.update_status()
    if not update:
        return []
    new_status = Generation.from_orm(update)
    return new_status.dict(), 201


@view_generation.put('/<int:uid>/complete')
def complete_generation(uid: int):
    update = storage.complete(uid=uid)
    complete = Generation.from_orm(update)
    return complete.dict(), 201
