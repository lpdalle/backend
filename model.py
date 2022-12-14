from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from db import Base, engine


class User(Base):
    __tablename__ = 'users'
    uid = Column("uid", UUID(as_uuid=True), primary_key=True)
    login = Column(String)
    email = Column(String(120), unique=True)

    def __repr__(self) -> str:
        return f'<User {self.login}>'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
