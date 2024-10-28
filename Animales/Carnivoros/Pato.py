from Animales.Animal import Animal
from Animales.Habilidades.Nadador import Nadador
from Animales.Habilidades.Volador import Volador

class Pato(Animal, Nadador, Volador):
    def __init__(self, especie, nivelEnergia, velocidad, ubicacion):
        super().__init__(especie, nivelEnergia, velocidad, ubicacion)