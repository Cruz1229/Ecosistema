from Plantas.Florales.PlantaFloral import PlantaFloral
import random

class Orquidero(PlantaFloral):
    def __init__(self, altura, edad, ubicacion, nivel_energia, nivel_agua):
        super().__init__(altura, edad, ubicacion, nivel_energia, nivel_agua)
        self.madurez_minima = 0.3
        self.TIEMPO_MINIMO_FLORACION = 60
        self.color_flores = random.choice(['rojo', 'rosa', 'blanco', 'amarillo'])

    def _calcular_produccion_flores(self) -> int:
        # La producción depende de la altura y condiciones
        produccion_base = int(self.altura * 2)
        factor_agua = min(1.0, self.nivel_agua / 100)
        factor_energia = min(1.0, self.nivel_energia / 100)

        produccion = produccion_base * factor_agua * factor_energia
        variacion = random.randint(-1, 1)
        return max(1, int(produccion) + variacion)

    def crecer(self):
        if self.nivel_agua >= 15 and self.nivel_energia >= 10:
            crecimiento = random.uniform(0.03, 0.08)  # Crecen más lento que los árboles
            self.altura += crecimiento
            self.nivel_agua -= 3
            self.nivel_energia -= 2
            return True
        return False

    def absorber_agua(self):
        if self.nivel_agua < 90:
            cantidad = min(15, 100 - self.nivel_agua)
            self.nivel_agua += cantidad
            return True
        return False

    def reproducirse(self):
        if self.nivel_energia >= 40 and self.altura >= self.madurez_minima:
            self.nivel_energia -= 20
            return True
        return False

    def perder_flores(self):
        """Método específico para simular la caída natural de flores"""
        if self.flores > 0 and random.random() < 0.1:  # 10% de probabilidad
            flores_perdidas = random.randint(1, max(1, self.flores // 3))
            self.flores = max(0, self.flores - flores_perdidas)
            return flores_perdidas
        return 0