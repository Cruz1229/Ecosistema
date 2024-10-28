from Plantas import Planta
from Plantas.Habilidades.Frutos import Frutos


class Manzano(Planta, Frutos):
    def __init__(self, altura, edad, ubicacion, nivel_energia, nivel_agua):
        super().__init__(altura, edad, ubicacion, nivel_energia, nivel_agua)

