from lpdalle.db import db_session
from lpdalle.errors import NotFoundError
from lpdalle.model import Generations


class GenerationsStorage:
    def get_by_uid(self, uid: int):
        gen = Generations.query.filter(Generations.uid == uid).first()
        if not gen:
            raise NotFoundError('Generation not found', str(uid))

        return gen

    def add(self, user_uid, promt, status):
        uid = None
        new_generation = Generations(uid=uid, user_uid=user_uid, promt=promt, status=status)
        db_session.add(new_generation)
        db_session.commit()
        return new_generation
