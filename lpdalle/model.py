from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lpdalle.db import Base, engine


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    # telegram_id = Column(String, index=True)
    login = Column(String, nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)  # noqa: WPS432
    generation = relationship('Generation', back_populates='user')

    def __repr__(self) -> str:
        return f'<User {self.login}, {self.email}>'


class Generation(Base):
    __tablename__ = 'generations'
    uid = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.uid'), index=True, nullable=False)
    prompt = Column(String, nullable=False)
    status = Column(String, index=True, nullable=False)
    user = relationship('User', back_populates='generation')

    def __repr__(self) -> str:
        return f'<Generation promt: {self.uid}: {self.prompt}>'


class Images(Base):
    __tablename__ = 'images'
    uid = Column(Integer, primary_key=True)
    url = Column(String, nullable=True)
    generation_id = Column(Integer, ForeignKey('generations.uid'), index=True, nullable=False)

    def __repr__(self) -> str:
        return f'<Image: {self.uid}: {self.url}>'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)


# GET <'/generations/id_gen/images/'>
# POST <'/generations/'> JSON
# POST <'/generations/id_gen/cancel>'>
# GET <'/generations/id_gen'>
