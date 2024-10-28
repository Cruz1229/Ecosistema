from Animales.Animal import Animal
from Animales.Carnivoros.Carnivoro import Carnivoro
from Animales.Habilidades.Volador import Volador
from Animales.Herbivoros.Ciervo import Ciervo
from Animales.Herbivoros.Conejo import Conejo


class Aguila_real(Animal, Volador, Carnivoro):
    def __init__(self, especie, nivelEnergia, velocidad, ubicacion):
        Animal.__init__(self, especie, nivelEnergia, velocidad, ubicacion)
        Carnivoro.__init__(self)
        self.rango_caza = 120

    def _calcular_probabilidad_caza(self, presa: 'Animal'):
        """Calcula la probabilidad de caza exitosa para el águila"""
        # Especialista en cazar conejos
        if isinstance(presa, Conejo):
            return 0.8
        # Menos efectiva contra presas grandes
        elif isinstance(presa, Ciervo):
            return 0.2
        # Probabilidad base para otras presas
        return 0.5