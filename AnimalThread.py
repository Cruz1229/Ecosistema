import threading
import time
import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class EventoEcosistema:
    """Clase que representa un evento en el ecosistema.

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


class AnimalThread(threading.Thread):
    """Clase que maneja el comportamiento concurrente de cada animal.

    Attributes:
        animal (Animal): Instancia del animal que maneja el thread.
        ecosistema (Ecosistema): Referencia al ecosistema en el que opera el animal.
        _paused (Event): Evento que controla la pausa del thread.
        _stopped (Event): Evento que controla la detención del thread.
    """

    def __init__(self, animal: 'Animal', ecosistema: 'Ecosistema'):
        """Inicializa el thread para un animal específico.

        Args:
            animal (Animal): Instancia del animal que manejará el thread.
            ecosistema (Ecosistema): Referencia al ecosistema en el que opera el animal.
        """
        super().__init__()
        self.animal = animal
        self.ecosistema = ecosistema
        self.daemon = True  # El thread se cerrará cuando el programa principal termine
        self._paused = threading.Event()  # Para pausar el thread
        self._stopped = threading.Event()  # Para detener el thread
        self._paused.set()  # Iniciar en estado activo

    def run(self):
        """Método principal que se ejecuta en el thread.

        Este método gestiona el ciclo de vida del thread del animal, realizando acciones
        mientras el animal esté vivo y el thread no esté detenido.
        """
        while not self._stopped.is_set():
            # Verificar si está pausado
            self._paused.wait()

            # Verificar si el animal está vivo
            if not self.animal.estar_vivo:
                self.stop()
                break

            # Realizar acciones del animal
            self.realizar_acciones()

            # Esperar un tiempo aleatorio antes de la siguiente acción
            time.sleep(random.uniform(0.5, 2.0))

    def realizar_acciones(self):
        """Ejecuta las acciones del animal según su tipo y estado.

        Esta función decide qué acción debe realizar el animal, como moverse, descansar,
        interactuar o buscar alimento, basado en su nivel de energía.
        """
        try:
            # Verificar energía
            if self.animal.nivel_energia < 30:
                self.buscar_alimento()
            else:
                # Realizar otras acciones
                accion = random.choice(['mover', 'descansar', 'interactuar', 'buscar_alimento'])
                if accion == 'mover':
                    self.mover()
                elif accion == 'descansar':
                    self.descansar()
                elif accion == 'interactuar':
                    self.interactuar()
                elif accion == 'buscar_alimento':
                    self.buscar_alimento()

        except Exception as e:
            print(f"Error en realizar_acciones: {str(e)}")

    def buscar_alimento(self):
        """Busca y consume alimento según el tipo de animal.

        Este método genera un evento que representa la búsqueda de alimento
        y simula un tiempo de búsqueda.
        """
        evento = EventoEcosistema(
            tipo='buscar_alimento',
            origen=self.animal,
            destino=None,
            datos={'tipo_animal': self.animal.__class__.__name__}
        )
        self.ecosistema.cola_eventos.put(evento)
        time.sleep(2)  # Simular tiempo de búsqueda

    def mover(self):
        """Mueve al animal a una nueva posición.

        Este método calcula una nueva posición aleatoria y genera un evento que
        representa el movimiento del animal.
        """
        x, y = self.animal.ubicacion
        dx = random.uniform(-10, 10)
        dy = random.uniform(-10, 10)
        nueva_pos = (x + dx, y + dy)

        evento = EventoEcosistema(
            tipo='mover',
            origen=self.animal,
            destino=nueva_pos,
            datos={'posicion_anterior': (x, y)}
        )
        self.ecosistema.cola_eventos.put(evento)

    def descansar(self):
        """El animal descansa y recupera energía.

        Este método genera un evento que representa el descanso del animal
        y simula un tiempo de descanso.
        """
        evento = EventoEcosistema(
            tipo='descansar',
            origen=self.animal,
            destino=None,
            datos={'energia_recuperada': 10}
        )
        self.ecosistema.cola_eventos.put(evento)
        time.sleep(4)

    def interactuar(self):
        """Interactúa con otros animales cercanos.

        Este método genera un evento que representa la interacción del animal
        con otros animales en un radio específico.
        """
        evento = EventoEcosistema(
            tipo='interactuar',
            origen=self.animal,
            destino=None,
            datos={'radio_busqueda': 50}
        )
        self.ecosistema.cola_eventos.put(evento)

    def pause(self):
        """Pausa el thread del animal.

        Este método establece el estado de pausa del thread, evitando que ejecute
        acciones hasta que sea reanudado.
        """
        self._paused.clear()

    def resume(self):
        """Reanuda el thread del animal.

        Este método permite que el thread ejecute acciones nuevamente.
        """
        self._paused.set()

    def stop(self):
        """Detiene el thread del animal.

        Este método establece el estado de detención del thread, finalizando
        su ejecución.
        """
        self._stopped.set()