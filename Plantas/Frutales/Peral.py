from Plantas.Frutales.PlantaFrutal import PlantaFrutal
import random

class Peral(PlantaFrutal):
    def __init__(self, altura, edad, ubicacion, nivel_energia, nivel_agua):
        super().__init__(altura, edad, ubicacion, nivel_energia, nivel_agua)
        self.madurez_minima = 1.5
        self.TIEMPO_MINIMO_FRUTOS = 120

    def _calcular_produccion_frutos(self) -> int:
        # Más altura = más frutos, con un componente aleatorio
        produccion_base = int(self.altura * 2)
        variacion = random.randint(-1, 2)
        return max(1, produccion_base + variacion)

    def absorber_agua(self):
        if self.nivel_agua < 80:
            cantidad = min(20, 100 - self.nivel_agua)
            self.nivel_agua += cantidad
            return True
        return False

    def reproducirse(self):
        if self.nivel_energia >= 60 and self.altura >= self.madurez_minima:
            self.nivel_energia -= 30
            return True
        return False