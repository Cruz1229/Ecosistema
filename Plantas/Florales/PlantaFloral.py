from abc import ABC, abstractmethod
from Plantas.Planta import Planta
import random

class PlantaFloral(Planta, ABC):
    """Clase base para plantas florales"""

    def __init__(self, altura, edad, ubicacion, nivel_energia, nivel_agua):
        super().__init__(altura, edad, ubicacion, nivel_energia, nivel_agua)
        self.flores = 0
        self.tiempo_entre_floracion = 0
        self.TIEMPO_MINIMO_FLORACION = 80
        self.ENERGIA_FLORACION = 8
        self.madurez_minima = 0.5  # Altura mínima para florecer

    def puede_florecer(self):
        """Verifica si la planta puede generar flores"""
        self.tiempo_entre_floracion += 1
        return (self.tiempo_entre_floracion >= self.TIEMPO_MINIMO_FLORACION and
                self.nivel_energia > self.ENERGIA_FLORACION and
                self.altura >= self.madurez_minima)

    def generar_flores(self):
        """
        Intenta generar flores si las condiciones son apropiadas.
        Returns:
            bool: True si generó flores, False en caso contrario
        """
        if not self.puede_florecer():
            return False

        # Verificar condiciones ambientales
        if self.nivel_agua < 20:
            return False

        # Gastar energía en la producción
        self.nivel_energia -= self.ENERGIA_FLORACION
        self.nivel_agua -= 3

        # Calcular cantidad de flores según la especie
        cantidad = self._calcular_produccion_flores()
        self.flores += cantidad

        # Reiniciar tiempo entre floraciones
        self.tiempo_entre_floracion = 0

        return True

    @abstractmethod
    def _calcular_produccion_flores(self) -> int:
        """
        Calcula la cantidad de flores a producir según el tipo de planta.
        Debe ser implementado por cada especie específica.
        """
        pass