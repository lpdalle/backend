from sqlalchemy.exc import IntegrityError

from lpdalle.db import db_session
from lpdalle.errors import ConflictError, NotFoundError
from lpdalle.model import Generation


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

    def update_status(self, status='pending'):
        generation = Generation.query.filter(Generation.status == status).first()
        if not generation:
            return []
        generation.status = 'running'
        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError('generation', generation.uid)
        return generation

    def complete(self, uid: int, status='complete'):
        generation = Generation.query.filter(Generation.uid == uid).first()
        generation.status = status
        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError('generation', generation.uid)
        return generation
