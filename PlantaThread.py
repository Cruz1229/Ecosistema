import threading
import time
import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class EventoEcosistema:
    tipo: str
    origen: Optional[object]
    destino: Optional[object]
    datos: dict

class PlantaThread(threading.Thread):
    """Clase que maneja el comportamiento concurrente de cada planta"""
    def __init__(self, planta: 'Planta', ecosistema: 'Ecosistema'):
        super().__init__()
        self.planta = planta
        self.ecosistema = ecosistema
        self.daemon = True
        self._paused = threading.Event()
        self._stopped = threading.Event()
        self._paused.set()

        # Constantes específicas para plantas
        self.TIEMPO_CRECIMIENTO = 200  # Ciclos necesarios para crecer
        self.TIEMPO_REPRODUCCION = 300  # Ciclos necesarios para reproducirse
        self.contador_crecimiento = 0
        self.contador_reproduccion = 0

    def run(self):
        """Método principal que se ejecuta en el thread"""
        while not self._stopped.is_set():
            self._paused.wait()

            if not self.planta.estar_vivo:
                self.stop()
                break

            # Realizar acciones de la planta
            self.realizar_acciones()

            # Esperar más tiempo que los animales ya que las plantas son más lentas
            time.sleep(random.uniform(1.0, 3.0))

    def realizar_acciones(self):
        """Ejecuta las acciones de la planta según su estado"""
        try:
            # Incrementar contadores
            self.contador_crecimiento += 1
            self.contador_reproduccion += 1

            # Verificar si necesita agua
            if self.planta.nivel_agua < 30:
                self.absorber_agua()

            # Crecer si es tiempo
            if self.contador_crecimiento >= self.TIEMPO_CRECIMIENTO:
                self.crecer()
                self.contador_crecimiento = 0

            # Reproducirse si es tiempo
            if self.contador_reproduccion >= self.TIEMPO_REPRODUCCION:
                self.reproducirse()
                self.contador_reproduccion = 0

            # Si es frutal, generar frutos
            if hasattr(self.planta, 'generar_frutos'):
                self.generar_frutos()

        except Exception as e:
            print(f"Error en realizar_acciones de planta: {str(e)}")

    def absorber_agua(self):
        """Absorbe agua del ecosistema"""
        evento = EventoEcosistema(
            tipo='absorber_agua',
            origen=self.planta,
            destino=None,
            datos={'cantidad_requerida': 10}
        )
        self.ecosistema.cola_eventos.put(evento)

    def crecer(self):
        """Hace crecer la planta"""
        evento = EventoEcosistema(
            tipo='crecer',
            origen=self.planta,
            destino=None,
            datos={'incremento_altura': 0.1}  # Incremento en metros
        )
        self.ecosistema.cola_eventos.put(evento)

    def reproducirse(self):
        """Intenta reproducir la planta"""
        evento = EventoEcosistema(
            tipo='reproducir_planta',
            origen=self.planta,
            destino=None,
            datos={
                'tipo_planta': self.planta.__class__.__name__,
                'radio_dispersion': 30  # Radio en píxeles para la nueva planta
            }
        )
        self.ecosistema.cola_eventos.put(evento)

    def generar_frutos(self):
        """Genera frutos si es una planta frutal"""
        if hasattr(self.planta, 'generar_frutos'):
            evento = EventoEcosistema(
                tipo='generar_frutos',
                origen=self.planta,
                destino=None,
                datos={'cantidad': random.randint(1, 5)}
            )
            self.ecosistema.cola_eventos.put(evento)

    def pause(self):
        """Pausa el thread de la planta"""
        self._paused.clear()

    def resume(self):
        """Reanuda el thread de la planta"""
        self._paused.set()

    def stop(self):
        """Detiene el thread de la planta"""
        self._stopped.set()