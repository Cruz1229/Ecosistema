from Animales.Animal import Animal

class Lince(Animal):
    def __init__(self, especie, nivelEnergia, velocidad, ubicacion):
        super().__init__(especie, nivelEnergia, velocidad, ubicacion)