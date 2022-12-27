from pydantic import BaseModel


class User(BaseModel):
    uid: int
    login: str
    email: str

    class Config:
        orm_mode = True


class Generations(BaseModel):
    uid: int
    user_id: int
    prompt: str
    status: str

    class Config:
        orm_mode = True
