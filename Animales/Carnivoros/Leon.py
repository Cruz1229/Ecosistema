from random import random
from Animales.Animal import Animal
from Animales.Carnivoros.Carnivoro import Carnivoro
from Animales.Herbivoros.Ciervo import Ciervo
from Animales.Herbivoros.Conejo import Conejo
from Animales.Herbivoros.Herbivoro import Herbivoro
from Decoradores.Decoradores import aumentar_velocidad


@aumentar_velocidad(incremento=50)  # Aumenta la velocidad en un 50%
class Leon(Animal, Carnivoro):
    def __init__(self, especie, nivelEnergia, velocidad, ubicacion):
        super().__init__(especie, nivelEnergia, velocidad, ubicacion)
        Carnivoro.__init__(self)
        self.rango_caza = 80  # Radio en el que puede detectar presas
        self.fuerza_ataque = 70  # Determina la probabilidad de éxito en la caza

    def _calcular_probabilidad_caza(self, presa: 'Animal'):
        """Calcula la probabilidad de caza exitosa para el león"""
        # Mayor probabilidad contra herbívoros grandes
        if isinstance(presa, Ciervo):
            return 0.7
        # Menor probabilidad contra presas pequeñas y rápidas
        elif isinstance(presa, Conejo):
            return 0.4
        # Probabilidad base para otras presas
        return 0.6

    def cazar(self, presa: 'Animal'):
        """
        Implementa la lógica de caza para el león.

        Args:
            presa: El animal que será cazado

        Returns:
            bool: True si la caza fue exitosa, False en caso contrario
        """
        if not isinstance(presa, Herbivoro):
            return False

        # Verificar si el león tiene suficiente energía para cazar
        if self.nivel_energia < 30:
            return False

        # Calcular probabilidad de éxito basada en la energía y fuerza del león
        probabilidad_exito = (self.nivel_energia / 100) * (self.fuerza_ataque / 100)

        # La caza consume energía independientemente del resultado
        self.nivel_energia = max(0, self.nivel_energia - 20)

        # Retornar el resultado de la caza
        return random() < probabilidad_exito