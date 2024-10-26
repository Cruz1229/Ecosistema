
from abc import ABC, abstractmethod

class Organismo(ABC):
    def __init__(self, ubicacion='', edad=0, peso=0, estar_vivo=True, nivel_energia=0):
        self._ubicacion = ubicacion
        self._edad = edad
        self._peso = peso
        self._estar_vivo = estar_vivo
        self._nivel_energia = nivel_energia

    @property
    def ubicacion(self):
        return self._ubicacion

    @property
    def edad(self):
        return self._edad

    @property
    def peso(self):
        return self._peso

    @property
    def estar_vivo(self):
        return self._estar_vivo

    @property
    def nivel_energia(self):
        return self._nivel_energia

    @ubicacion.setter
    def ubicacion(self, ubicacion):
        self._ubicacion = ubicacion

    @nivel_energia.setter
    def nivel_energia(self, nivel_energia):
        self._nivel_energia = nivel_energia

    @edad.setter
    def edad(self, edad):
        self._edad = edad

    @peso.setter
    def peso(self,peso):
        self._peso = peso

    @estar_vivo.setter
    def estar_vivo(self, estar_vivo):
        self._estar_vivo = estar_vivo

    @abstractmethod
    def alimentarse(self):
        pass

    @abstractmethod
    def reproducirse(self):
        pass