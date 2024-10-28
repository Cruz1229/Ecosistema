from abc import ABC, abstractmethod

class Frutos(ABC):
    def __init__(self):
        self._frutos = 0

    @property
    def frutos(self):
        return self._frutos

    @frutos.setter
    def frutos(self, value):
        self._frutos = value

    @abstractmethod
    def generar_frutos(self):
        pass