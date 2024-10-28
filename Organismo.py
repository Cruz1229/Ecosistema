from abc import ABC, abstractmethod


class Organismo(ABC):
    """Clase base abstracta para todos los organismos del ecosistema.

    Esta clase define la estructura básica y comportamiento que deben tener
    todos los organismos vivos dentro del ecosistema, incluyendo sus propiedades
    básicas y métodos esenciales para la supervivencia.

    Attributes:
        ubicacion (tuple): Coordenadas (x, y) de la posición del organismo.
        edad (int): Edad actual del organismo.
        peso (float): Peso actual del organismo.
        estar_vivo (bool): Estado vital del organismo.
        nivel_energia (float): Nivel actual de energía del organismo.
    """

    def __init__(self, ubicacion='', edad=0, peso=0, estar_vivo=True, nivel_energia=0):
        """Inicializa una nueva instancia de Organismo.

        Args:
            ubicacion (tuple, opcional): Coordenadas iniciales. Defaults to ''.
            edad (int, opcional): Edad inicial del organismo. Defaults to 0.
            peso (float, opcional): Peso inicial del organismo. Defaults to 0.
            estar_vivo (bool, opcional): Estado vital inicial. Defaults to True.
            nivel_energia (float, opcional): Energía inicial. Defaults to 0.
        """
        self._ubicacion = ubicacion
        self._edad = edad
        self._peso = peso
        self._estar_vivo = estar_vivo
        self._nivel_energia = nivel_energia

    @property
    def ubicacion(self):
        """tuple: Obtiene las coordenadas actuales del organismo."""
        return self._ubicacion

    @property
    def edad(self):
        """int: Obtiene la edad actual del organismo."""
        return self._edad

    @property
    def peso(self):
        """float: Obtiene el peso actual del organismo."""
        return self._peso

    @property
    def estar_vivo(self):
        """bool: Obtiene el estado vital actual del organismo."""
        return self._estar_vivo

    @property
    def nivel_energia(self):
        """float: Obtiene el nivel actual de energía del organismo."""
        return self._nivel_energia

    @ubicacion.setter
    def ubicacion(self, ubicacion):
        """Establece la nueva ubicación del organismo.

        Args:
            ubicacion (tuple): Nuevas coordenadas (x, y).
        """
        self._ubicacion = ubicacion

    @nivel_energia.setter
    def nivel_energia(self, nivel_energia):
        """Establece el nuevo nivel de energía del organismo.

        Args:
            nivel_energia (float): Nuevo nivel de energía.
        """
        self._nivel_energia = nivel_energia

    @edad.setter
    def edad(self, edad):
        """Establece la nueva edad del organismo.

        Args:
            edad (int): Nueva edad.
        """
        self._edad = edad

    @peso.setter
    def peso(self, peso):
        """Establece el nuevo peso del organismo.

        Args:
            peso (float): Nuevo peso.
        """
        self._peso = peso

    @estar_vivo.setter
    def estar_vivo(self, estar_vivo):
        """Establece el nuevo estado vital del organismo.

        Args:
            estar_vivo (bool): Nuevo estado vital.
        """
        self._estar_vivo = estar_vivo

    @abstractmethod
    def alimentarse(self):
        """Método abstracto que define el comportamiento de alimentación.

        Este método debe ser implementado por las clases hijas para definir
        cómo cada tipo específico de organismo obtiene su alimento.

        Raises:
            NotImplementedError: Si la clase hija no implementa este método.
        """
        pass

    @abstractmethod
    def reproducirse(self):
        """Método abstracto que define el comportamiento de reproducción.

        Este método debe ser implementado por las clases hijas para definir
        cómo cada tipo específico de organismo se reproduce.

        Raises:
            NotImplementedError: Si la clase hija no implementa este método.
        """
        pass