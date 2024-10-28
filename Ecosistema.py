import threading
import random
from typing import List, Dict, Tuple, Optional
from abc import ABC
from queue import Queue
from AnimalThread import AnimalThread
from Animales.Animal import Animal
from Animales.Carnivoros.Aguila_real import Aguila_real
from Animales.Carnivoros.Carnivoro import Carnivoro
from Animales.Carnivoros.Leon import Leon
from Animales.Herbivoros.Ciervo import Ciervo
from Animales.Herbivoros.Conejo import Conejo
from Animales.Herbivoros.Herbivoro import Herbivoro
from PlantaThread import PlantaThread
from Plantas.Planta import Planta
from dataclasses import dataclass


@dataclass
class EventoEcosistema:
    """Clase para representar un evento en el ecosistema.

    Attributes:
        tipo (str): Tipo de evento.
        origen (Optional[object]): Entidad que genera el evento.
        destino (Optional[object]): Entidad que es el destino del evento.
        datos (dict): Información adicional sobre el evento.
    """
    tipo: str
    origen: Optional[object]
    destino: Optional[object]
    datos: dict

class Ecosistema:
    """Clase principal que maneja el ecosistema y sus entidades.

    Attributes:
        tamano (Tuple[float, float]): Tamaño del ecosistema.
        carnivoros (Dict[str, List[Animal]]): Diccionario de carnívoros por especie.
        herbivoros (Dict[str, List[Animal]]): Diccionario de herbívoros por especie.
        plantas (Dict[str, List[Planta]]): Diccionario de plantas por especie.
        frutales (Dict[str, List[Planta]]): Diccionario de plantas frutales por especie.
        florales (Dict[str, List[Planta]]): Diccionario de plantas florales por especie.
        MIN_ANIMALES_POR_ESPECIE (int): Mínimo de animales por especie.
        threads (List[AnimalThread, PlantaThread]): Lista de threads para entidades.
        cola_eventos (Queue): Cola para eventos del ecosistema.
        thread_procesador (Thread): Thread que procesa eventos.
        lock (RLock): Monitor para sincronización.
        recursos (dict): Recursos disponibles en el ecosistema.
    """

    def __init__(self, tamano: Tuple[float, float] = (1000, 1000)):
        """Inicializa un ecosistema con el tamaño especificado.

        Args:
            tamano (Tuple[float, float], optional): Tamaño del ecosistema.
                Por defecto es (1000, 1000).
        """
        self.tamano = tamano
        self.carnivoros: Dict[str, List[Animal]] = {}
        self.herbivoros: Dict[str, List[Animal]] = {}
        self.plantas: Dict[str, List[Planta]] = {}
        self.frutales: Dict[str, List[Planta]] = {}
        self.florales: Dict[str, List[Planta]] = {}

        # Mínimo de animales por especie
        self.MIN_ANIMALES_POR_ESPECIE = 2

        # Control de threads
        self.threads: List[AnimalThread, PlantaThread] = []
        self.cola_eventos: Queue = Queue()
        self.thread_procesador = threading.Thread(target=self.procesar_eventos)
        self.thread_procesador.daemon = True
        self.thread_procesador.start()

        # Monitor para sincronización
        self.lock = threading.RLock()

        # Estado del ecosistema
        self.recursos = {
            'agua': 100.0,
            'vegetacion': 100.0,
            'temperatura': 25.0,
            'humedad': 60.0
        }

    def verificar_poblacion_minima(self):
        """Verifica y mantiene la población mínima de cada especie."""
        with self.lock:
            # Verificar carnívoros
            for especie, lista in self.carnivoros.items():
                animales_vivos = [a for a in lista if a.estar_vivo]
                if len(animales_vivos) < self.MIN_ANIMALES_POR_ESPECIE:
                    self.repoblar_especie(especie, self.MIN_ANIMALES_POR_ESPECIE - len(animales_vivos))

            # Verificar herbívoros
            for especie, lista in self.herbivoros.items():
                animales_vivos = [a for a in lista if a.estar_vivo]
                if len(animales_vivos) < self.MIN_ANIMALES_POR_ESPECIE:
                    self.repoblar_especie(especie, self.MIN_ANIMALES_POR_ESPECIE - len(animales_vivos))

    def repoblar_especie(self, especie: str, cantidad: int):
        """Repobla una especie específica con la cantidad indicada.

        Args:
            especie (str): Nombre de la especie a repoblar.
            cantidad (int): Cantidad de animales a agregar.
        """
        for _ in range(cantidad):
            # Generar posición aleatoria
            x = random.uniform(0, self.tamano[0])
            y = random.uniform(0, self.tamano[1])

            # Crear nuevo animal según la especie
            nuevo_animal = None
            tipo = ''

            if especie == 'Leon':
                nuevo_animal = Leon("Leon", 100, 2.0, (x, y))
                tipo = 'carnivoro'
            elif especie == 'Aguila_real':
                nuevo_animal = Aguila_real("Aguila", 100, 3.0, (x, y))
                tipo = 'carnivoro'
            elif especie == 'Conejo':
                nuevo_animal = Conejo("Conejo", 100, 4.0, (x, y))
                tipo = 'herbivoro'
            elif especie == 'Ciervo':
                nuevo_animal = Ciervo("Ciervo", 100, 3.0, (x, y))
                tipo = 'herbivoro'

            if nuevo_animal:
                self.agregar_entidad(nuevo_animal, tipo)

    def agregar_entidad(self, entidad: ABC, tipo: str) -> bool:
        """Agrega una nueva entidad al ecosistema y crea su thread si es un animal.

        Args:
            entidad (ABC): Entidad a agregar al ecosistema.
            tipo (str): Tipo de la entidad ('carnivoro', 'herbivoro', 'frutal', 'floral').

        Returns:
            bool: True si la entidad fue agregada exitosamente, False en caso contrario.
        """
        with self.lock:
            try:
                # Agregar la entidad a la lista correspondiente
                if tipo == 'carnivoro':
                    especie = entidad.__class__.__name__
                    if especie not in self.carnivoros:
                        self.carnivoros[especie] = []
                    self.carnivoros[especie].append(entidad)
                    # Crear y comenzar thread para el carnívoro
                    thread = AnimalThread(entidad, self)
                    self.threads.append(thread)
                    thread.start()

                elif tipo == 'herbivoro':
                    especie = entidad.__class__.__name__
                    if especie not in self.herbivoros:
                        self.herbivoros[especie] = []
                    self.herbivoros[especie].append(entidad)
                    # Crear y comenzar thread para el herbívoro
                    thread = AnimalThread(entidad, self)
                    self.threads.append(thread)
                    thread.start()

                elif tipo == 'frutal':
                    especie = entidad.__class__.__name__
                    if especie not in self.frutales:
                        self.frutales[especie] = []
                    self.frutales[especie].append(entidad)
                    thread = PlantaThread(entidad, self)
                    self.threads.append(thread)
                    thread.start()

                elif tipo == 'floral':
                    especie = entidad.__class__.__name__
                    if especie not in self.florales:
                        self.florales[especie] = []
                    self.florales[especie].append(entidad)
                    thread = PlantaThread(entidad, self)
                    self.threads.append(thread)
                    thread.start()

                return True
            except Exception as e:
                print(f"Error al agregar entidad: {str(e)}")
                return False

    def procesar_eventos(self):
        """Procesa los eventos generados por los threads de los animales."""
        while True:
            evento = self.cola_eventos.get()
            with self.lock:
                try:
                    if evento.tipo == 'buscar_alimento':
                        self.procesar_busqueda_alimento(evento)
                    elif evento.tipo == 'mover':
                        self.procesar_movimiento(evento)
                    elif evento.tipo == 'descansar':
                        self.procesar_descanso(evento)
                    elif evento.tipo == 'interactuar':
                        self.procesar_interaccion(evento)
                    elif evento.tipo == 'absorber_agua':
                        self.procesar_absorcion_agua(evento)
                    elif evento.tipo == 'crecer':
                        self.procesar_crecimiento(evento)
                    elif evento.tipo == 'generar_frutos':
                        self.procesar_generacion_frutos(evento)
                    elif evento.tipo == 'reproducir_planta':
                        self.procesar_reproduccion_planta(evento)
                except Exception as e:
                    print(f"Error al procesar evento: {str(e)}")

    # Procesadores de eventos
    def procesar_busqueda_alimento(self, evento: EventoEcosistema):
        """Procesa el evento de búsqueda de alimento.

        Args:
            evento (EventoEcosistema): Evento a procesar.
        """
        pass  # Implementación de la lógica

    def procesar_movimiento(self, evento: EventoEcosistema):
        """Procesa el evento de movimiento.

        Args:
            evento (EventoEcosistema): Evento a procesar.
        """
        pass  # Implementación de la lógica

    def procesar_descanso(self, evento: EventoEcosistema):
        """Procesa el evento de descanso.

        Args:
            evento (EventoEcosistema): Evento a procesar.
        """
        pass  # Implementación de la lógica

    def procesar_interaccion(self, evento: EventoEcosistema):
        """Procesa el evento de interacción.

        Args:
            evento (EventoEcosistema): Evento a procesar.
        """
        pass  # Implementación de la lógica

    def procesar_absorcion_agua(self, evento: EventoEcosistema):
        """Procesa el evento de absorción de agua.

        Args:
            evento (EventoEcosistema): Evento a procesar.
        """
        pass  # Implementación de la lógica

    def procesar_crecimiento(self, evento: EventoEcosistema):
        """Procesa el evento de crecimiento.

        Args:
            evento (EventoEcosistema): Evento a procesar.
        """
        pass  # Implementación de la lógica

    def procesar_generacion_frutos(self, evento: EventoEcosistema):
        """Procesa el evento de generación de frutos.

        Args:
            evento (EventoEcosistema): Evento a procesar.
        """
        pass  # Implementación de la lógica

    def procesar_reproduccion_planta(self, evento: EventoEcosistema):
        """Procesa el evento de reproducción de planta.

        Args:
            evento (EventoEcosistema): Evento a procesar.
        """
        pass  # Implementación de la lógica