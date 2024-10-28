from abc import ABC, abstractmethod
from typing import Optional, Dict, Tuple
import math
import random

class Carnivoro(ABC):
    """Clase base para animales carnívoros"""

    def __init__(self):
        self.tiempo_entre_caza = 0
        self.TIEMPO_MINIMO_ENTRE_CAZA = 100
        self.rango_caza = 80  # Rango de caza por defecto
        self.ENERGIA_CAZA = 10  # Energía que gasta al cazar

    def puede_cazar(self):
        """Verifica si el animal puede realizar una caza"""
        self.tiempo_entre_caza += 1
        return (self.tiempo_entre_caza >= self.TIEMPO_MINIMO_ENTRE_CAZA and
                self.nivel_energia > self.ENERGIA_CAZA)

    def cazar(self, presa: 'Animal'):
        """
        Intenta cazar a una presa.

        Args:
            presa: Animal objetivo de la caza

        Returns:
            bool: True si la caza fue exitosa, False en caso contrario
        """
        if not self.puede_cazar():
            return False

        # Calcular distancia a la presa
        dx = self.ubicacion[0] - presa.ubicacion[0]
        dy = self.ubicacion[1] - presa.ubicacion[1]
        distancia = math.sqrt(dx*dx + dy*dy)

        # Verificar si está en rango de caza
        if distancia > self.rango_caza:
            return False

        # Gastar energía en el intento de caza
        self.nivel_energia -= self.ENERGIA_CAZA

        # Probabilidad de caza exitosa (puede ser personalizada por cada especie)
        probabilidad_exito = self._calcular_probabilidad_caza(presa)
        caza_exitosa = random.random() < probabilidad_exito

        # Reiniciar tiempo entre caza
        self.tiempo_entre_caza = 0

        return caza_exitosa

    @abstractmethod
    def _calcular_probabilidad_caza(self, presa: 'Animal'):
        """
        Calcula la probabilidad de éxito en la caza según el tipo de carnívoro y presa.
        Debe ser implementado por cada especie específica.
        """
        pass