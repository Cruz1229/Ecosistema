import math
import random
from typing import Dict, Optional
from Animales.Carnivoros.Carnivoro import Carnivoro
from Organismo import Organismo


class Animal(Organismo):
    ENERGIA_MAXIMA = 100

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
        self._direccion = random.uniform(0, 2 * math.pi)  # Dirección aleatoria inicial
        self.ENERGIA_POR_PRESA: Dict[str, float] = {
            'Conejo': 40,
            'Ciervo': 60,
            'Pato': 30,
            'Capibara': 50
        }

    @property
    def especie(self):
        return self._especie

    @property
    def velocidad(self):
        return self._velocidad

    @property
    def direccion(self):
        return self._direccion

    @especie.setter
    def especie(self, especie):
        self._especie = especie

    @velocidad.setter
    def velocidad(self, velocidad):
        self._velocidad = velocidad

    @direccion.setter
    def direccion(self, nueva_direccion):
        self._direccion = nueva_direccion

    def alimentarse(self, presa: Optional['Animal'] = None):
        """
        Procesa la alimentación del animal.
        Para carnívoros requiere una presa, para herbívoros puede ser None.

        Args:
            presa: Animal que será consumido (solo para carnívoros)

        Returns:
            bool: True si la alimentación fue exitosa
        """
        try:
            if isinstance(self, Carnivoro):
                if not presa or not presa.estar_vivo:
                    return False

                # Obtener energía según el tipo de presa
                energia_ganada = self.ENERGIA_POR_PRESA.get(
                    presa.__class__.__name__, 30)

                # Actualizar energía del depredador
                self.nivel_energia = min(
                    self.ENERGIA_MAXIMA,
                    self.nivel_energia + energia_ganada
                )

                # Eliminar la presa
                presa.estar_vivo = False
                del presa

                return True

            else:  # Herbívoro
                # Lógica para herbívoros (consumo de vegetación)
                if self.ecosistema and self.ecosistema.recursos['vegetacion'] > 10:
                    self.ecosistema.recursos['vegetacion'] -= 10
                    self.nivel_energia = min(
                        self.ENERGIA_MAXIMA,
                        self.nivel_energia + 20
                    )
                    return True

            return False

        except Exception as e:
            print(f"Error en alimentarse: {str(e)}")
            return False

    def reproducirse(self):
        print('Animal reproduciendoce')

    def moverse(self, ancho_limite: float, alto_limite: float):
        """
        Mueve al animal en una dirección con posible cambio aleatorio y
        retorna la nueva posición respetando los límites del ecosistema.

        Args:
            ancho_limite: Ancho máximo del área de movimiento
            alto_limite: Alto máximo del área de movimiento

        Returns:
            Tuple[float, float]: Nueva posición (x, y) del animal
        """
        # Posibilidad de cambiar dirección
        if random.random() < 0.1:  # 10% de probabilidad de cambiar dirección
            self._direccion += random.uniform(-math.pi/4, math.pi/4)

        # Calcular nuevo movimiento
        dx = math.cos(self._direccion) * self._velocidad
        dy = math.sin(self._direccion) * self._velocidad

        # Obtener nueva posición
        nuevo_x = self.ubicacion[0] + dx
        nuevo_y = self.ubicacion[1] + dy

        # Verificar límites y rebotar si es necesario
        if nuevo_x < 0 or nuevo_x > ancho_limite:
            self._direccion = math.pi - self._direccion
            nuevo_x = max(0, min(ancho_limite, nuevo_x))

        if nuevo_y < 0 or nuevo_y > alto_limite:
            self._direccion = -self._direccion
            nuevo_y = max(0, min(alto_limite, nuevo_y))

        # Actualizar posición
        self.ubicacion = (nuevo_x, nuevo_y)

        # Consumir energía por movimiento
        self.nivel_energia -= 0.1
        if self.nivel_energia < 0:
            self.estar_vivo = False

        return self.ubicacion
