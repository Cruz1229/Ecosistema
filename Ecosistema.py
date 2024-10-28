import threading
from typing import List, Dict, Tuple, Optional
from abc import ABC
from queue import Queue
from AnimalThread import AnimalThread
from Animales.Animal import Animal
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

        # Control de threads
        self.threads: List[AnimalThread] = []
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

    def agregar_entidad(self, entidad: ABC, tipo: str) -> bool:
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

                elif tipo == 'planta':
                    especie = entidad.__class__.__name__
                    if especie not in self.plantas:
                        self.plantas[especie] = []
                    self.plantas[especie].append(entidad)

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