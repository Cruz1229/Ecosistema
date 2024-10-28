from abc import ABC, abstractmethod


class Herbivoro(ABC):
    ENERGIA_POR_FRUTO = 15  # Energía ganada por cada fruto consumido
    DISTANCIA_ALIMENTACION = 30  # Distancia máxima para alimentarse de una planta

    @abstractmethod
    def huir(self):
        pass

    def buscar_planta_cercana(self, plantas: list, pos_actual: tuple):
        """
        Busca la planta frutal más cercana al herbívoro.

        Args:
            plantas: Lista de plantas en el ecosistema
            pos_actual: Posición actual del herbívoro (x, y)

        Returns:
            Tuple[Planta, float]: La planta más cercana y la distancia a ella
        """
        planta_cercana = None
        menor_distancia = float('inf')

        for planta in plantas:
            if not planta.estar_vivo:
                continue

            dx = pos_actual[0] - planta.ubicacion[0]
            dy = pos_actual[1] - planta.ubicacion[1]
            distancia = (dx*dx + dy*dy)**0.5

            if distancia < menor_distancia:
                menor_distancia = distancia
                planta_cercana = planta

        return planta_cercana, menor_distancia

    def alimentarse_de_planta(self, planta: 'Planta'):
        """
        Intenta alimentarse de una planta frutal.

        Args:
            planta: Planta objetivo

        Returns:
            bool: True si logró alimentarse, False en caso contrario
        """
        if not planta or not planta.estar_vivo:
            return False

        # Verificar si es una planta frutal y tiene frutos
        if hasattr(planta, 'frutos') and planta.frutos > 0:
            # Consumir frutos y ganar energía
            frutos_consumidos = min(3, planta.frutos)  # Máximo 3 frutos por vez
            planta.frutos -= frutos_consumidos
            energia_ganada = frutos_consumidos * self.ENERGIA_POR_FRUTO

            # Actualizar energía del herbívoro
            self.nivel_energia = min(100, self.nivel_energia + energia_ganada)
            return True

        return False