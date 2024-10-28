from Animales.Animal import Animal

class Conejo(Animal):
    def __init__(self, especie, nivelEnergia, velocidad, ubicacion):
        super().__init__(especie, nivelEnergia, velocidad, ubicacion)

    def huir(self):
        print("Conejo huyendo")
