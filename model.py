from sqlalchemy import Column, String, Integer
from db import Base, engine


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    login = Column(String)
    email = Column(String(120), unique=True)

    def __repr__(self) -> str:
        return f'<User id={self.uid}, login={self.login}, email={self.email}>'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
