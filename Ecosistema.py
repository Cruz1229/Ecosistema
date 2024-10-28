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
    tipo: str
    origen: Optional[object]
    destino: Optional[object]
    datos: dict

class Ecosistema:
    """Clase principal que maneja el ecosistema y sus entidades"""
    def __init__(self, tamano: Tuple[float, float] = (1000, 1000)):
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
        """Verifica y mantiene la población mínima de cada especie"""
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
        """Repobla una especie específica con la cantidad indicada"""
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

    def agregar_entidad(self, entidad: ABC, tipo: str):
        """Agrega una nueva entidad al ecosistema y crea su thread si es un animal"""
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
        """Procesa los eventos generados por los threads de los animales"""
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
                    # Verificar población mínima después de cada evento
                    self.verificar_poblacion_minima()

                except Exception as e:
                    print(f"Error procesando evento {evento.tipo}: {str(e)}")
            self.cola_eventos.task_done()

    def procesar_busqueda_alimento(self, evento: EventoEcosistema):
        """Procesa la búsqueda de alimento de un animal"""
        animal = evento.origen
        if isinstance(animal, Carnivoro):
            # Buscar presa
            presa = self.encontrar_presa_cercana(animal)
            if presa and presa.estar_vivo:
                animal.nivel_energia += 30
                presa.estar_vivo = False
                print(f"{animal.__class__.__name__} cazó a {presa.__class__.__name__}")
        elif isinstance(animal, Herbivoro):
            # Buscar vegetación
            if self.recursos['vegetacion'] > 10:
                self.recursos['vegetacion'] -= 10
                animal.nivel_energia += 20
                print(f"{animal.__class__.__name__} se alimentó de vegetación")

    def procesar_movimiento(self, evento: EventoEcosistema):
        """Procesa el movimiento de un animal"""
        animal = evento.origen
        nueva_pos = evento.destino

        # Verificar límites del ecosistema
        x = max(0, min(self.tamano[0], nueva_pos[0]))
        y = max(0, min(self.tamano[1], nueva_pos[1]))

        animal.ubicacion = (x, y)
        animal.nivel_energia -= 5
        print(f"{animal.__class__.__name__} se movió a ({x:.1f}, {y:.1f})")

    def procesar_descanso(self, evento: EventoEcosistema):
        """Procesa el descanso de un animal"""
        animal = evento.origen
        energia_recuperada = evento.datos['energia_recuperada']
        animal.nivel_energia = min(100, animal.nivel_energia + energia_recuperada)
        print(f"{animal.__class__.__name__} descansó y recuperó energía")

    def procesar_interaccion(self, evento: EventoEcosistema):
        """Procesa la interacción entre animales"""
        animal = evento.origen
        radio = evento.datos['radio_busqueda']

        # Encontrar animales cercanos
        cercanos = self.encontrar_animales_cercanos(animal, radio)
        if cercanos:
            print(f"{animal.__class__.__name__} interactuó con {len(cercanos)} animales cercanos")

    def encontrar_presa_cercana(self, depredador: 'Animal', radio: float = 50.0) -> Optional['Animal']:
        """Encuentra una presa cercana para un depredador"""
        for especies in self.herbivoros.values():
            for presa in especies:
                if presa.estar_vivo:
                    distancia = self.calcular_distancia(depredador.ubicacion, presa.ubicacion)
                    if distancia < radio:
                        return presa
        return None

    def encontrar_animales_cercanos(self, animal: 'Animal', radio: float) -> List['Animal']:
        """Encuentra otros animales cercanos"""
        cercanos = []
        todas_especies = {**self.carnivoros, **self.herbivoros}

        for especies in todas_especies.values():
            for otro_animal in especies:
                if otro_animal != animal and otro_animal.estar_vivo:
                    distancia = self.calcular_distancia(animal.ubicacion, otro_animal.ubicacion)
                    if distancia < radio:
                        cercanos.append(otro_animal)
        return cercanos

    def calcular_distancia(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calcula la distancia entre dos puntos"""
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

    def procesar_absorcion_agua(self, evento: EventoEcosistema):
        """Procesa la absorción de agua por una planta"""
        planta = evento.origen
        cantidad = evento.datos.get('cantidad_requerida', 10)

        if self.recursos['agua'] >= cantidad:
            self.recursos['agua'] -= cantidad
            planta.nivel_agua += cantidad
            print(f"{planta.__class__.__name__} absorbió {cantidad} de agua")

    def procesar_crecimiento(self, evento: EventoEcosistema):
        """Procesa el crecimiento de una planta"""
        planta = evento.origen
        incremento = evento.datos.get('incremento_altura', 0.1)

        if planta.nivel_agua > 20:
            planta.altura += incremento
            planta.nivel_agua -= 5
            print(f"{planta.__class__.__name__} creció {incremento}m")

    def procesar_generacion_frutos(self, evento: EventoEcosistema):
        """Procesa la generación de frutos"""
        planta = evento.origen
        cantidad = evento.datos.get('cantidad', 1)

        if hasattr(planta, 'frutos'):
            planta.frutos += cantidad
            print(f"{planta.__class__.__name__} generó {cantidad} frutos")

    def procesar_reproduccion_planta(self, evento: EventoEcosistema):
        """Procesa la reproducción de una planta"""
        planta = evento.origen
        radio = evento.datos.get('radio_dispersion', 30)

        # La lógica de creación de nuevas plantas se maneja en la GUI
        print(f"{planta.__class__.__name__} intentó reproducirse")

    def pausar_simulacion(self):
        """Pausa todos los threads de animales"""
        for thread in self.threads:
            thread.pause()

    def reanudar_simulacion(self):
        """Reanuda todos los threads de animales"""
        for thread in self.threads:
            thread.resume()

    def detener_simulacion(self):
        """Detiene todos los threads de animales"""
        for thread in self.threads:
            thread.stop()
        self.threads.clear()