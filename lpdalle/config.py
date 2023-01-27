import os
from dataclasses import dataclass


@dataclass
class Config:
    elephant_url: str
    port: str


def load() -> Config:
    return Config(
        elephant_url=os.environ['ELEPHANT_URL'],
        port=os.environ['PORT'],
    )


conf = load()
