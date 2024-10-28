from abc import ABC, abstractmethod
from Plantas.Planta import Planta
import random

class PlantaFrutal(Planta, ABC):
    """Clase base para plantas frutales"""

    def __init__(self, altura, edad, ubicacion, nivel_energia, nivel_agua):
        super().__init__(altura, edad, ubicacion, nivel_energia, nivel_agua)
        self.frutos = 0
        self.tiempo_entre_frutos = 0
        self.TIEMPO_MINIMO_FRUTOS = 100
        self.ENERGIA_PRODUCCION = 10
        self.madurez_minima = 1.0  # Altura mínima para dar frutos

    def puede_generar_frutos(self):
        """Verifica si la planta puede generar frutos"""
        self.tiempo_entre_frutos += 1
        return (self.tiempo_entre_frutos >= self.TIEMPO_MINIMO_FRUTOS and
                self.nivel_energia > self.ENERGIA_PRODUCCION and
                self.altura >= self.madurez_minima)

    def generar_frutos(self):
        """
        Intenta generar frutos si las condiciones son apropiadas.
        Returns:
            bool: True si generó frutos, False en caso contrario
        """
        if not self.puede_generar_frutos():
            return False

        # Verificar condiciones ambientales
        if self.nivel_agua < 30:
            return False

        # Gastar energía en la producción
        self.nivel_energia -= self.ENERGIA_PRODUCCION
        self.nivel_agua -= 5

        # Calcular cantidad de frutos según la especie
        cantidad = self._calcular_produccion_frutos()
        self.frutos += cantidad

        # Reiniciar tiempo entre producción
        self.tiempo_entre_frutos = 0

        return True

    @abstractmethod
    def _calcular_produccion_frutos(self) -> int:
        """
        Calcula la cantidad de frutos a producir según el tipo de árbol.
        Debe ser implementado por cada especie específica.
        """
        pass

    def obtener_frutos(self) -> int:
        """Recoge y retorna los frutos disponibles"""
        frutos_disponibles = self.frutos
        self.frutos = 0
        return frutos_disponibles

    def crecer(self):
        """Implementación base del crecimiento para plantas frutales"""
        if self.nivel_agua >= 20 and self.nivel_energia >= 15:
            crecimiento = random.uniform(0.05, 0.15)  # Crecimiento variable
            self.altura += crecimiento
            self.nivel_agua -= 5
            self.nivel_energia -= 5
            return True
        return False