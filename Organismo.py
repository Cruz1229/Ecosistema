from abc import ABC, abstractmethod
from typing import Any


class Organismo(ABC):
    """
    Clase base abstracta que define las características básicas de un organismo en el ecosistema.

    Esta clase sirve como plantilla para todos los seres vivos del sistema, definiendo
    sus atributos básicos y comportamientos comunes.

    Attributes:
        _ubicacion: Posición del organismo en el ecosistema
        _edad: Edad del organismo en unidades de tiempo
        _peso: Peso del organismo
        _estar_vivo: Estado vital del organismo
        _nivel_energia: Nivel actual de energía del organismo (0-100)
    """

    def __init__(self, ubicacion='', edad=0, peso=0, estar_vivo=True, nivel_energia=0):
        """
        Inicializa un nuevo organismo con los valores proporcionados.

        Args:
            ubicacion: Posición inicial del organismo. Valor por defecto: ''
            edad: Edad inicial del organismo. Valor por defecto: 0
            peso: Peso inicial del organismo. Valor por defecto: 0
            estar_vivo: Estado vital inicial. Valor por defecto: True
            nivel_energia: Nivel de energía inicial. Valor por defecto: 0
        """
        self._ubicacion = ubicacion
        self._edad = edad
        self._peso = peso
        self._estar_vivo = estar_vivo
        self._nivel_energia = nivel_energia

    @property
    def ubicacion(self) -> Any:
        """Obtiene la ubicación actual del organismo."""
        return self._ubicacion

    @property
    def edad(self) -> int:
        """Obtiene la edad actual del organismo."""
        return self._edad

    @property
    def peso(self) -> float:
        """Obtiene el peso actual del organismo."""
        return self._peso

    @property
    def estar_vivo(self) -> bool:
        """Obtiene el estado vital actual del organismo."""
        return self._estar_vivo

    @property
    def nivel_energia(self) -> float:
        """Obtiene el nivel actual de energía del organismo."""
        return self._nivel_energia

    @ubicacion.setter
    def ubicacion(self, ubicacion: Any) -> None:
        """Establece la nueva ubicación del organismo."""
        self._ubicacion = ubicacion

    @nivel_energia.setter
    def nivel_energia(self, nivel_energia: float) -> None:
        """
        Establece el nivel de energía del organismo.

        Args:
            nivel_energia: Nuevo nivel de energía a establecer.
            Se normaliza automáticamente entre 0 y 100.
        """
        if nivel_energia < 0:
            self._nivel_energia = 0
        elif nivel_energia > 100:
            self._nivel_energia = 100
        else:
            self._nivel_energia = nivel_energia

    @edad.setter
    def edad(self, edad: int) -> None:
        """
        Establece la edad del organismo.

        Args:
            edad: Nueva edad del organismo.
            Se valida que no sea negativa.
        """
        if edad < 0:
            raise ValueError("La edad no puede ser negativa")
        self._edad = edad

    @peso.setter
    def peso(self, peso: float) -> None:
        """
        Establece el peso del organismo.

        Args:
            peso: Nuevo peso del organismo.
            Se valida que no sea negativo.
        """
        if peso < 0:
            raise ValueError("El peso no puede ser negativo")
        self._peso = peso

    @estar_vivo.setter
    def estar_vivo(self, estar_vivo: bool) -> None:
        """
        Establece el estado vital del organismo.

        Args:
            estar_vivo: Nuevo estado vital (True = vivo, False = muerto)
        """
        self._estar_vivo = bool(estar_vivo)

    @abstractmethod
    def alimentarse(self) -> None:
        """
        Método abstracto que define el comportamiento de alimentación.
        Debe ser implementado por las clases hijas.
        """
        pass

    @abstractmethod
    def reproducirse(self) -> None:
        """
        Método abstracto que define el comportamiento de reproducción.
        Debe ser implementado por las clases hijas.
        """
        pass