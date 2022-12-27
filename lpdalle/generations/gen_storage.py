from sqlalchemy.exc import IntegrityError

from lpdalle.db import db_session
from lpdalle.errors import ConflictError, NotFoundError
from lpdalle.model import Generations


class GenerationsStorage:
    def get_by_uid(self, uid: int):
        gen = Generations.query.filter(Generations.uid == uid).first()
        if not gen:
            raise NotFoundError('Generation not found', str(uid))

        return gen

    def add(self, user_id: int, prompt: str, status: str) -> Generations:
        new_generation = Generations(user_id=user_id, prompt=prompt, status=status)
        db_session.add(new_generation)

        try:
            db_session.commit()
        except IntegrityError:
            raise ConflictError('users', new_generation.uid)

        return new_generation
