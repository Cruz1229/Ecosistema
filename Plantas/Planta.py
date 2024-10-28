from Organismo import Organismo
from abc import ABC, abstractmethod


class Planta(Organismo, ABC):  # Agregar ABC aquí
    def __init__(self, altura, edad, ubicacion, nivel_energia, nivel_agua):
        super().__init__(ubicacion=ubicacion, edad=edad, nivel_energia=nivel_energia)
        self._altura = altura
        self._nivel_agua = nivel_agua

    @property
    def altura(self):
        return self._altura

    @property
    def edad(self):
        return self._edad

    @property
    def nivel_agua(self):
        return self._nivel_agua

    @altura.setter
    def altura(self, altura):
        self._altura = altura

    @edad.setter
    def edad(self, edad):
        self._edad = edad

    @nivel_agua.setter
    def nivel_agua(self, nivel_agua):
        self._nivel_agua = nivel_agua

    @abstractmethod
    def crecer(self):
        pass

    @abstractmethod
    def absorber_agua(self):
        pass

    def alimentarse(self):
        self.absorber_agua()