import os
from dataclasses import dataclass


@dataclass
class Config:
    db_key: str
    port: str


def load() -> Config:
    return Config(
        db_key=os.environ['DB_KEY'],
        port=os.environ['PORT'],
    )


conf = load()
