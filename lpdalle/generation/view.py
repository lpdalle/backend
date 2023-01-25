from pathlib import Path
from uuid import uuid4

from flask import Blueprint, request

from lpdalle.errors import BadRequestError
from lpdalle.generation.storage import GenerationStorage
from lpdalle.schemas import Generation, Images

view_generation = Blueprint('generations', __name__)
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


@view_generation.post('/acquire')
def acquire():
    update = storage.acquire()
    if not update:
        return []
    new_status = Generation.from_orm(update)
    return new_status.dict(), 201


@view_generation.post('/<int:uid>/complete')
def complete_generation(uid: int):
    update = storage.complete(uid=uid)
    complete = Generation.from_orm(update)
    return complete.dict(), 201


IMAGES = Path('.data/images')


@view_generation.post('/<int:uid>/images/')
def upload_file(uid: int):
    dir = IMAGES / str(uid)
    dir.mkdir(parents=True, exist_ok=True)
    filename = f'{uuid4().hex}.png'
    filepath = dir / filename

    file = request.files['file']
    content = file.read()
    with open(filepath, 'wb') as fs:
        fs.write(content)

    image_url_add = storage.add_url(
        url=str(filepath),
        generation_id=uid,
    )
    record_image = Images.from_orm(image_url_add)
    return {record_image.url: 'File saved'}, 201


@view_generation.get('/<int:uid>/image')
def get_image(uid: int):
    file_url = storage.get_file(uid)[0]
    with open(file_url, 'rb') as fs:
        return fs.read()
