from pydantic import BaseModel


class User(BaseModel):
    uid: int
    login: str
    email: str

    class Config:
        orm_mode = True
