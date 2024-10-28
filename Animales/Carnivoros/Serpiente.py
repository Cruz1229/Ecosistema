from Animales.Animal import Animal

class Serpiente(Animal):
    def __init__(self, especie, nivelEnergia, velocidad, ubicacion):
        super().__init__(especie, nivelEnergia, velocidad, ubicacion)

    def arrastrarse(self):
        print('Serpiente arrastrandose')
