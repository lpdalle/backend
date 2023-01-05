from sqlalchemy.exc import IntegrityError

from lpdalle.db import db_session
from lpdalle.errors import ConflictError, NotFoundError
from lpdalle.model import Generation, User


class GenerationStorage:
    def get_by_uid(self, uid: int) -> Generation:
        gen = Generation.query.filter(Generation.uid == uid).first()
        if not gen:
            raise NotFoundError('Generation not found', str(uid))

        return gen

    def get_by_telegram_id(self, telegram_id: str) -> list[Generation]:
        user = db_session.query(User.uid)
        user = user.filter(User.telegram_id == telegram_id).first()

        gens = Generation.query.filter(Generation.user_id == user[0])
        gens = gens.all()
        if not gens:
            raise NotFoundError('Generations not found', telegram_id)
        return gens

    def get_user_generations(self, user_id: int) -> list[Generation]:
        gens = Generation.query.filter(Generation.user_id == user_id)
        gens = gens.all()
        if not gens:
            raise NotFoundError('Generations not found', str(user_id))

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
