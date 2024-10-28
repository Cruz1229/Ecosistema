import math
import random
from typing import Dict, Optional, List, Tuple


from Animales.Carnivoros.Carnivoro import Carnivoro
from Organismo import Organismo


class Animal(Organismo):
    ENERGIA_MAXIMA = 100
    ENERGIA_MINIMA_MOVIMIENTO = 10
    ENERGIA_MINIMA_REPRODUCCION = 40
    COSTO_ENERGIA_REPRODUCCION = 30
    DISTANCIA_REPRODUCCION = 50
    PROBABILIDAD_REPRODUCCION = 0.2

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
        self._direccion = random.uniform(0, 2 * math.pi)
        self._tiempo_reproduccion = 0
        self.TIEMPO_MINIMO_REPRODUCCION = {
            'Leon': 700,
            'Aguila_real': 600,
            'Conejo': 400,
            'Ciervo': 500
        }.get(especie, 500)

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
    def direccion(self, direccion):
        self._direccion = direccion

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

    def reproducirse(self, otros_animales: List['Animal']) -> Optional['Animal']:
        """
        Intenta reproducirse con otro animal de la misma especie si se cumplen las condiciones.
        """
        # Incrementar contador de tiempo
        self._tiempo_reproduccion += 1

        # Verificar condiciones básicas
        if (self._tiempo_reproduccion < self.TIEMPO_MINIMO_REPRODUCCION or
                self.nivel_energia < self.ENERGIA_MINIMA_REPRODUCCION):
            return None

        # Buscar pareja compatible
        for otro_animal in otros_animales:
            if (otro_animal != self and
                    type(otro_animal) == type(self) and
                    otro_animal.estar_vivo and
                    otro_animal.nivel_energia >= self.ENERGIA_MINIMA_REPRODUCCION and
                    otro_animal._tiempo_reproduccion >= otro_animal.TIEMPO_MINIMO_REPRODUCCION):

                # Calcular distancia
                dx = self.ubicacion[0] - otro_animal.ubicacion[0]
                dy = self.ubicacion[1] - otro_animal.ubicacion[1]
                distancia = math.sqrt(dx*dx + dy*dy)

                # Verificar distancia y probabilidad
                if (distancia <= self.DISTANCIA_REPRODUCCION and
                        random.random() < self.PROBABILIDAD_REPRODUCCION):

                    # Posición para el nuevo animal
                    pos_x = (self.ubicacion[0] + otro_animal.ubicacion[0]) / 2 + random.uniform(-20, 20)
                    pos_y = (self.ubicacion[1] + otro_animal.ubicacion[1]) / 2 + random.uniform(-20, 20)

                    # Crear nuevo animal
                    nuevo_animal = self._crear_cria((pos_x, pos_y))

                    if nuevo_animal:
                        # Aplicar costo de energía a los padres
                        self.nivel_energia -= self.COSTO_ENERGIA_REPRODUCCION
                        otro_animal.nivel_energia -= self.COSTO_ENERGIA_REPRODUCCION

                        # Reiniciar contadores
                        self._tiempo_reproduccion = 0
                        otro_animal._tiempo_reproduccion = 0

                        return nuevo_animal

        return None

    def _crear_cria(self, ubicacion: Tuple[float, float]) -> Optional['Animal']:
        """
        Crea una nueva instancia del animal según su tipo.
        """
        try:
            # Obtener el nombre de la clase actual
            clase_nombre = self.__class__.__name__

            # Configuración para cada tipo de animal
            configs = {
                'Leon': ('Leon', 100, 2.0),
                'Aguila_real': ('Aguila', 100, 3.0),
                'Conejo': ('Conejo', 100, 4.0),
                'Ciervo': ('Ciervo', 100, 3.0)
            }

            if clase_nombre in configs:
                especie, energia, velocidad = configs[clase_nombre]
                # Crear una nueva instancia usando la misma clase del animal actual
                return self.__class__(especie, energia, velocidad, ubicacion)

            return None

        except Exception as e:
            print(f"Error al crear cría: {str(e)}")
            return None

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
        if self.nivel_energia >= self.ENERGIA_MINIMA_MOVIMIENTO:
            # Posibilidad de cambiar dirección
            if random.random() < 0.1:
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
            self.nivel_energia = max(0, self.nivel_energia - 0.1)

    def descansar(self):
        """
        El animal descansa y recupera energía gradualmente.
        """
        energia_recuperada = 5  # Recupera 5 puntos de energía por descanso
        self.nivel_energia = min(self.ENERGIA_MAXIMA, self.nivel_energia + energia_recuperada)