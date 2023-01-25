from sqlalchemy.exc import IntegrityError

from lpdalle.db import db_session
from lpdalle.errors import ConflictError, NotFoundError
from lpdalle.model import Generation, Images


class GenerationStorage:
    def get_by_uid(self, uid: int) -> Generation:
        gen = Generation.query.filter(Generation.uid == uid).first()
        if not gen:
            raise NotFoundError('Generation not found', str(uid))

        return gen

    def get_user_generations(self, user_id: int) -> list[Generation]:
        gens = Generation.query.filter(Generation.user_id == user_id)
        gens = gens.all()
        if not gens:
            return []
        return gens

    def add(self, user_id: int, prompt: str, status: str) -> Generation:
        new_generation = Generation(
            user_id=user_id,
            prompt=prompt,
            status=status,
        )
        db_session.add(new_generation)

        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError('generation', new_generation.uid)

        return new_generation

    def add_url(self, url: str, generation_id: int):
        image_url = Images(
            url=url,
            generation_id=generation_id,
        )
        db_session.add(image_url)

        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError('generation', image_url.generation_id)

        return image_url

    def get_file(self, generation_id: int):
        file_url = db_session.query(Images.url)
        file_url = file_url.filter(Images.generation_id == generation_id).first()
        if not file_url:
            return []
        return file_url

    def acquire(self, status='pending'):
        generation = Generation.query.filter(Generation.status == status).first()
        if not generation:
            return []
        generation.status = 'running'
        db_session.commit()
        return generation

    def complete(self, uid: int, status='complete'):
        generation = Generation.query.filter(Generation.uid == uid).first()
        generation.status = status
        db_session.commit()
        return generation

