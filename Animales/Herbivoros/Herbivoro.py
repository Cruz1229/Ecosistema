from abc import ABC, abstractmethod


class Herbivoro(ABC):

    @abstractmethod
    def huir(self):
        pass