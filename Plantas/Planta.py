from Organismo import Organismo


class Planta(Organismo):
    def __init__(self, altura, edad, ubicacion, nivel_energia, nivel_agua):
        self._altura = altura
        self._edad = edad
        self._nivel_agua = nivel_agua
        super().__init__(ubicacion, nivel_energia)

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
    def altura (self, altura):
        self._altura = altura

    @edad.setter
    def edad (self, edad):
        self._edad = edad

    @nivel_agua.setter
    def nivel_agua(self, nivel_agua):
        self._nivel_energia = nivel_agua

    def crecer(self):
        print("Planta creciendo")

    def reproducirse(self):
        print("Planta reproduciendose")

    def absorber_agua(self):
        print("absorbiendo agua desde las raíces")