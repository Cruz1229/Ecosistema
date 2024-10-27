from Organismo import Organismo


class Animal(Organismo):
    def __init__(self, especie, nivelEnergia, velocidad, ubicacion):
        super().__init__(
            ubicacion=ubicacion,
            nivel_energia=nivelEnergia,
            edad=0,
            peso=0,
            estar_vivo=True
        )
        self._especie = especie
        self._velocidad = velocidad


    @property
    def especie(self):
        return self._especie

    @property
    def velocidad(self):
        return self._velocidad

    @especie.setter
    def especie(self, especie):
        self._especie = especie

    @velocidad.setter
    def velocidad(self, velocidad):
        self._velocidad = velocidad

    def alimentarse(self):
        print('Aminal alimentandose')

    def reproducirse(self):
        print('Animal reproduciendoce')

    def moverse(self):
        print('Animal moviendose')
