from Animales.Animal import Animal
from Animales.Habilidades.Nadador import Nadador


class Capibara(Animal, Nadador):
    def __init__(self, especie, nivelEnergia, velocidad, ubicacion):
        super().__init__(especie, nivelEnergia, velocidad, ubicacion)

