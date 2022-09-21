from models.lession import Lession
from dataclasses import dataclass

@dataclass
class Day():
    name: str
    lessions: list[Lession]