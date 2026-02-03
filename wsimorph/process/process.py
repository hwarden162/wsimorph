from abc import ABC, abstractmethod

from ..image._tile import Tile


class ABCProcess(ABC):

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string.")
        if len(name) == 0:
            raise ValueError("name cannot be an empty string.")
        self._name = name

    @abstractmethod
    def run(self, tile: Tile) -> Tile:
        pass

    @staticmethod
    @abstractmethod
    def from_config(self, config: dict) -> "ABCProcess":
        pass

    @abstractmethod
    def to_config(self) -> dict:
        pass

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"<Process: {self.name}>"
