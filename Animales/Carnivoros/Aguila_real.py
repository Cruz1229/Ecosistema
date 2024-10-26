from Animales import Animal
from Animales.Habilidades.Volador import Volador

class Aguila_real(Animal, Volador):
    def __init__(self, especie, nivelEnergia, velocidad, ubicacion):
        super().__init__(especie, nivelEnergia, velocidad, ubicacion)