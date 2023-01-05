from pydantic import BaseModel


class User(BaseModel):
    uid: int
    login: str
    email: str
    telegram_id: str

    class Config:
        orm_mode = True


class Generation(BaseModel):
    uid: int
    user_id: int
    prompt: str
    status: str

    class Config:
        orm_mode = True
