import math

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QGraphicsScene, QGraphicsView,
                             QMessageBox, QLabel, QHBoxLayout, QListWidget, QSplitter, QFrame, QDialog)
from PyQt6.QtGui import QPixmap, QBrush, QPen, QColor
from PyQt6.QtCore import Qt, QTimer, QRectF, QTime
import sys
import os
import random
from typing import Dict, List
from Animales.Carnivoros.Carnivoro import Carnivoro
from Animales.Habilidades.Nadador import Nadador
from Animales.Habilidades.Volador import Volador
from Animales.Herbivoros.Herbivoro import Herbivoro
from Ecosistema import Ecosistema
from Animales.Animal import Animal
from Animales.Carnivoros.Leon import Leon
from Animales.Carnivoros.Aguila_real import Aguila_real
from Animales.Herbivoros.Conejo import Conejo
from Animales.Herbivoros.Ciervo import Ciervo
from GestorEstado import GestorEstado
from Plantas.Florales.Cempasuchil import Cempasuchil
from Plantas.Florales.Orquidero import Orquidero
from Plantas.Florales.Rosal import Rosal
from Plantas.Frutales.Manzano import Manzano
from Plantas.Frutales.Naranjo import Naranjo
from Plantas.Frutales.Peral import Peral


class AnimalGraphicsItem:
    """Clase para manejar la representación gráfica de cada animal"""
    def __init__(self, animal: 'Animal', imagen_path: str):
        self.animal = animal
        self.imagen_path = imagen_path
        self.pixmap = None
        self.cargar_imagen()
        # self.direccion = random.uniform(0, 2 * math.pi)  # Dirección aleatoria inicial
        # self.velocidad = random.uniform(1, 3)  # Velocidad aleatoria
        self.tiempo_reproduccion = 0  # Contador para reproducción
        self.tiempo_entre_caza = 0
        self.TIEMPO_MINIMO_ENTRE_CAZA = 100  # Ciclos mínimos entre cacerías
        self.ultima_presa = None  # Para seguimiento de la presa

    def mover(self, width: int, height: int):
        """Delega el movimiento al objeto animal"""
        self.animal.moverse(width, height)

    def puede_cazar(self):
        """Verifica si el animal puede cazar"""
        return (isinstance(self.animal, Carnivoro) and
                self.tiempo_entre_caza >= self.TIEMPO_MINIMO_ENTRE_CAZA)

    def es_presa_valida(self, presa: 'Animal'):
        """Verifica si un animal es una presa válida según el depredador"""
        if isinstance(self.animal, Leon):
            return isinstance(presa, Herbivoro)
        elif isinstance(self.animal, Aguila_real):
            return isinstance(presa, Conejo)
        return False

    def cargar_imagen(self):
        try:
            if os.path.exists(self.imagen_path):
                self.pixmap = QPixmap(self.imagen_path).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
            else:
                self.pixmap = QPixmap(30, 30)
                self.pixmap.fill(QColor(random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255)))
        except Exception as e:
            print(f"Error al cargar imagen {self.imagen_path}: {str(e)}")
            self.pixmap = QPixmap(30, 30)
            self.pixmap.fill(QColor(255, 0, 0))

    # def mover(self, width: int, height: int):
    #     """Mueve al animal en una dirección con posible cambio aleatorio"""
    #     # Posibilidad de cambiar dirección
    #     if random.random() < 0.1:  # 10% de probabilidad de cambiar dirección
    #         self.direccion += random.uniform(-math.pi/4, math.pi/4)
    #
    #     # Calcular nuevo movimiento
    #     dx = math.cos(self.direccion) * self.velocidad
    #     dy = math.sin(self.direccion) * self.velocidad
    #
    #     # Obtener nueva posición
    #     nuevo_x = self.animal.ubicacion[0] + dx
    #     nuevo_y = self.animal.ubicacion[1] + dy
    #
    #     # Verificar límites y rebotar si es necesario
    #     if nuevo_x < 0 or nuevo_x > width:
    #         self.direccion = math.pi - self.direccion
    #         nuevo_x = max(0, min(width, nuevo_x))
    #     if nuevo_y < 0 or nuevo_y > height:
    #         self.direccion = -self.direccion
    #         nuevo_y = max(0, min(height, nuevo_y))
    #
    #     # Actualizar posición
    #     self.animal.ubicacion = (nuevo_x, nuevo_y)
    #
    #     # Consumir energía por movimiento
    #     self.animal.nivel_energia -= 0.1
    #     if self.animal.nivel_energia < 0:
    #         self.animal.estar_vivo = False

    @property
    def x(self):
        return self.animal.ubicacion[0] if self.animal else 0

    @property
    def y(self):
        return self.animal.ubicacion[1] if self.animal else 0

class PlantaGraphicsItem:
    """Clase para manejar la representación gráfica de cada planta"""
    def __init__(self, planta: 'Planta', imagen_path: str):
        self.planta = planta
        self.imagen_path = imagen_path
        self.pixmap = None
        self.cargar_imagen()
        self.tiempo_crecimiento = 0
        self.tiempo_reproduccion = 0

    def cargar_imagen(self):
        try:
            if os.path.exists(self.imagen_path):
                # Escalar según la altura de la planta
                tamano_base = 30
                factor_escala = min(2.0, max(1.0, self.planta.altura))
                tamano = int(tamano_base * factor_escala)

                self.pixmap = QPixmap(self.imagen_path).scaled(
                    tamano, tamano,
                    Qt.AspectRatioMode.KeepAspectRatio
                )
            else:
                self.pixmap = QPixmap(30, 30)
                self.pixmap.fill(QColor(34, 139, 34))  # Verde forestal por defecto
        except Exception as e:
            print(f"Error al cargar imagen {self.imagen_path}: {str(e)}")
            self.pixmap = QPixmap(30, 30)
            self.pixmap.fill(QColor(0, 255, 0))

    @property
    def x(self):
        return self.planta.ubicacion[0] if self.planta else 0

    @property
    def y(self):
        return self.planta.ubicacion[1] if self.planta else 0

class EcosistemaGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulación de Ecosistema")
        self.setGeometry(100, 100, 1200, 800)

        # Constantes del ecosistema
        self.ANCHO_ECOSISTEMA = 1000
        self.ALTO_ECOSISTEMA = 600
        self.DISTANCIA_REPRODUCCION = 50

        # Parámetros de reproducción ajustados
        self.TIEMPO_MINIMO_REPRODUCCION = 1  # Aumentado significativamente
        self.PROBABILIDAD_REPRODUCCION = 100 # 20% de probabilidad cuando se cumplan las condiciones
        self.ENERGIA_MINIMA_REPRODUCCION = 20  # Energía mínima necesaria para reproducirse
        self.COSTO_ENERGIA_REPRODUCCION = 10  # Energía que cuesta reproducirse

        # Contadores de tiempo específicos por especie
        self.TIEMPOS_REPRODUCCION = {
            'Leon': 400,         # Más tiempo para carnívoros grandes
            'Aguila_real': 350,
            'Conejo': 200,       # Menor tiempo para herbívoros pequeños
            'Ciervo': 250
        }

        self.ENERGIA_GANADA_CAZA = {
            'Conejo': 40,
            'Ciervo': 60
        }

        # Crear el ecosistema
        self.ecosistema = None

        # Diccionario para almacenar las imágenes de los animales
        self.imagenes_animales: Dict[str, str] = {
            'Leon': 'imagenes/leon.png',
            'Aguila_real': 'imagenes/aguila.png',
            'Lince': 'imagenes/lince.png',
            'Lobo_gris': 'imagenes/lobo.png',
            'Serpiente': 'imagenes/serpiente.png',
            'Pato': 'imagenes/pato.png',
            'Capibara': 'imagenes/capibara.png',
            'Ciervo': 'imagenes/ciervo.png',
            'Conejo': 'imagenes/conejo.png',
            'Tapir': 'imagenes/tapir.png'
        }

        self.imagenes_plantas: Dict[str, str] = {
            'Manzano': 'imagenes/manzano.png',
            'Naranjo': 'imagenes/naranjo.png',
            'Peral': 'imagenes/peral.png',
            'Rosal': 'imagenes/rosal.png',
            'Orquidero': 'imagenes/orquidero.png',
            'Cempasuchil': 'imagenes/cempasuchil.png'

        }

        # Lista para plantas
        self.planta_items = []

        # Parámetros para plantas
        self.TIEMPO_MINIMO_REPRODUCCION_PLANTAS = 10000000
        self.PROBABILIDAD_REPRODUCCION_PLANTAS = 0.001
        self.DISTANCIA_REPRODUCCION_PLANTAS = 150

        # Representaciones gráficas de los animales
        self.animal_items = []

        # Timer para actualizar la visualización
        self.timer = None

        # Agregar lista de animales
        self.lista_animales = QListWidget()
        self.lista_animales.setMaximumWidth(300)  # Ancho máximo del panel lateral

        # Agregar lista para registrar acciones
        self.lista_acciones = QListWidget()
        self.lista_acciones.setMaximumHeight(200)  # Limitar altura del registro
        self.max_acciones = 100  # Máximo número de acciones a mostrar

        # Configurar la interfaz
        self.setup_ui()

        # Verificar directorio de imágenes
        self.verificar_directorio_imagenes()

        self.imagenes_plantas: Dict[str, str] = {
            'Manzano': 'imagenes/manzano.png',
            'Naranjo': 'imagenes/naranjo.png',
            'Peral': 'imagenes/peral.png',
            'Rosal': 'imagenes/rosal.png',
            'Orquidero': 'imagenes/orquidero.png',
            'Cempasuchil': 'imagenes/cempasuchil.png'

        }

        # Lista para plantas
        self.planta_items = []

        # Inicializar el gestor de estado
        self.gestor_estado = GestorEstado()

    def verificar_cazas(self):
        """Verifica y procesa las cazas entre depredadores y presas"""
        for depredador in self.animal_items:
            if not depredador.animal.estar_vivo or not isinstance(depredador.animal, Carnivoro):
                continue

            # Buscar presas cercanas
            presa_cercana = None
            menor_distancia = float('inf')

            for presa in self.animal_items:
                if (not presa.animal.estar_vivo or
                        presa.animal == depredador.animal or
                        not isinstance(presa.animal, Herbivoro)):
                    continue

                # Calcular distancia
                dx = depredador.x - presa.x
                dy = depredador.y - presa.y
                distancia = math.sqrt(dx*dx + dy*dy)

                if distancia < depredador.animal.rango_caza and distancia < menor_distancia:
                    presa_cercana = presa
                    menor_distancia = distancia

            # Si encontró una presa, intentar cazar
            if presa_cercana:
                self.realizar_caza(depredador.animal, presa_cercana.animal)

    def crear_plantas_iniciales(self):
        """Crea las plantas iniciales en el ecosistema"""
        try:
            def generar_posicion():
                return (
                    random.uniform(50, self.ANCHO_ECOSISTEMA - 50),
                    random.uniform(50, self.ALTO_ECOSISTEMA - 50)
                )

            # Crear instancias de plantas
            plantas = [
                (Manzano(1.0, 0, generar_posicion(), 100, 100), 'frutal'),
                (Manzano(1.0, 0, generar_posicion(), 100, 100), 'frutal'),
                (Naranjo(1.0, 0, generar_posicion(), 100, 100), 'frutal'),
                (Naranjo(1.0, 0, generar_posicion(), 100, 100), 'frutal'),
                (Peral(1.0, 0, generar_posicion(), 100, 100), 'frutal'),
                (Peral(1.0, 0, generar_posicion(), 100, 100), 'frutal'),
                (Rosal(0.5, 0, generar_posicion(), 100, 100), 'floral'),
                (Rosal(0.5, 0, generar_posicion(), 100, 100), 'floral'),
                (Orquidero(0.5, 0, generar_posicion(), 100, 100), 'floral'),
                (Orquidero(0.5, 0, generar_posicion(), 100, 100), 'floral'),
                (Cempasuchil(0.5, 0, generar_posicion(), 100, 100), 'floral'),
                (Cempasuchil(0.5, 0, generar_posicion(), 100, 100), 'floral'),


                # Agregar más tipos de plantas según necesites
            ]

            # Agregar cada planta al ecosistema
            for planta, tipo in plantas:
                self.ecosistema.agregar_entidad(planta, tipo)
                especie = planta.__class__.__name__
                if especie in self.imagenes_plantas:
                    item = PlantaGraphicsItem(planta, self.imagenes_plantas[especie])
                    self.planta_items.append(item)

        except Exception as e:
            raise Exception(f"Error al crear plantas: {str(e)}")

    def realizar_caza(self, depredador: Animal, presa: Animal):
        """Procesa el intento de caza"""
        # Intentar cazar
        if depredador.cazar(presa):
            # Si la caza fue exitosa, alimentarse
            if depredador.alimentarse(presa):
                self.lbl_estado.setText(
                    f"Estado: {depredador.__class__.__name__} cazó y se alimentó de {presa.__class__.__name__}"
                )
                self.registrar_accion(
                    depredador.__class__.__name__,
                    "Cazar",
                    f"Cazó exitosamente a un {presa.__class__.__name__}"
                )
        else:
            # Caza fallida
            self.lbl_estado.setText(
                f"Estado: {depredador.__class__.__name__} falló la caza"
            )
            self.registrar_accion(
                depredador.__class__.__name__,
                "Cazar",
                "Intento fallido"
            )
            # Hacer que la presa huya
            self.hacer_huir_presa(presa)

    def hacer_huir_presa(self, presa: AnimalGraphicsItem):
        """Hace que la presa huya cuando la caza falla"""
        # Implementar el método huir si existe en la clase Herbívoro
        if isinstance(presa.animal, Herbivoro):
            presa.animal.huir()
            self.registrar_accion(
                presa.__class__.__name__,
                "Huir",
                "Escapó de un depredador"
            )

        # Cambiar dirección y aumentar velocidad temporalmente
        presa.direccion = random.uniform(0, 2 * math.pi)
        velocidad_original = presa.velocidad
        presa.velocidad *= 1.5

        # Gastar energía al huir
        presa.animal.nivel_energia = max(0, presa.animal.nivel_energia - 5)

        # Restaurar velocidad después de un tiempo
        def restaurar_velocidad():
            presa.velocidad = velocidad_original

        QTimer.singleShot(2000, restaurar_velocidad)  # 2 segundos de huida

    def verificar_reproduccion(self):
        """Verifica si hay animales cercanos que puedan reproducirse"""
        nuevos_animales = []

        for i, item1 in enumerate(self.animal_items):
            if not item1.animal.estar_vivo:
                continue

            # Incrementar el tiempo de reproducción
            item1.tiempo_reproduccion += 1
            especie = item1.animal.__class__.__name__
            tiempo_minimo = self.TIEMPOS_REPRODUCCION.get(especie, self.TIEMPO_MINIMO_REPRODUCCION)

            # Verificar condiciones básicas para reproducción
            if (item1.tiempo_reproduccion < tiempo_minimo or
                    item1.animal.nivel_energia < self.ENERGIA_MINIMA_REPRODUCCION):
                continue

            for item2 in self.animal_items[i+1:]:
                if not item2.animal.estar_vivo:
                    continue

                # Verificar si son de la misma especie y tienen suficiente energía
                if (type(item1.animal) == type(item2.animal) and
                        item2.tiempo_reproduccion >= tiempo_minimo and
                        item2.animal.nivel_energia >= self.ENERGIA_MINIMA_REPRODUCCION):

                    # Calcular distancia
                    dx = item1.x - item2.x
                    dy = item1.y - item2.y
                    distancia = math.sqrt(dx*dx + dy*dy)

                    # Verificar distancia y probabilidad
                    if (distancia <= self.DISTANCIA_REPRODUCCION and
                            random.random() < self.PROBABILIDAD_REPRODUCCION):

                        # Posición para el nuevo animal (con algo de variación)
                        pos_x = (item1.x + item2.x) / 2 + random.uniform(-20, 20)
                        pos_y = (item1.y + item2.y) / 2 + random.uniform(-20, 20)

                        # Mantener dentro de los límites
                        pos_x = max(0, min(self.ANCHO_ECOSISTEMA, pos_x))
                        pos_y = max(0, min(self.ALTO_ECOSISTEMA, pos_y))

                        # Crear nuevo animal según la especie
                        nuevo_animal = None
                        if isinstance(item1.animal, Leon):
                            nuevo_animal = Leon(especie, 100, 2.0, (pos_x, pos_y))
                        elif isinstance(item1.animal, Aguila_real):
                            nuevo_animal = Aguila_real(especie, 100, 3.0, (pos_x, pos_y))
                        elif isinstance(item1.animal, Conejo):
                            nuevo_animal = Conejo(especie, 100, 4.0, (pos_x, pos_y))
                        elif isinstance(item1.animal, Ciervo):
                            nuevo_animal = Ciervo(especie, 100, 3.0, (pos_x, pos_y))

                        if nuevo_animal:
                            # Determinar tipo
                            tipo = 'carnivoro' if isinstance(nuevo_animal, (Leon, Aguila_real)) else 'herbivoro'
                            nuevos_animales.append((nuevo_animal, tipo))

                            # Aplicar costo de energía a los padres
                            item1.animal.nivel_energia -= self.COSTO_ENERGIA_REPRODUCCION
                            item2.animal.nivel_energia -= self.COSTO_ENERGIA_REPRODUCCION

                            # Reiniciar contadores de reproducción
                            item1.tiempo_reproduccion = 0
                            item2.tiempo_reproduccion = 0

                            # Mostrar mensaje de nacimiento
                            self.lbl_estado.setText(f"Estado: Nuevo {especie} ha nacido!")

        # Agregar nuevos animales al ecosistema
        for animal, tipo in nuevos_animales:
            self.ecosistema.agregar_entidad(animal, tipo)
            if animal.__class__.__name__ in self.imagenes_animales:
                item = AnimalGraphicsItem(animal, self.imagenes_animales[animal.__class__.__name__])
                self.animal_items.append(item)

    def verificar_reproduccion_plantas(self):
        nuevas_plantas = []

        for i, item1 in enumerate(self.planta_items):
            if not item1.planta.estar_vivo:
                continue

            # Incrementar el tiempo de reproducción
            item1.tiempo_reproduccion += 1

            # Verificar si la planta puede reproducirse
            if random.random() < self.PROBABILIDAD_REPRODUCCION_PLANTAS:
                # Generar nueva posición cerca de la planta madre
                radio = self.DISTANCIA_REPRODUCCION_PLANTAS
                angulo = random.uniform(0, 2 * math.pi)

                pos_x = item1.x + radio * math.cos(angulo)
                pos_y = item1.y + radio * math.sin(angulo)

                # Mantener dentro de los límites
                pos_x = max(0, min(self.ANCHO_ECOSISTEMA, pos_x))
                pos_y = max(0, min(self.ALTO_ECOSISTEMA, pos_y))

                # Crear nueva planta según la especie
                nueva_planta = None
                tipo = None

                if isinstance(item1.planta, Manzano):
                    nueva_planta = Manzano(0.5, 0, (pos_x, pos_y), 100, 100)
                    tipo = 'frutal'
                elif isinstance(item1.planta, Naranjo):
                    nueva_planta = Naranjo(0.5, 0, (pos_x, pos_y), 100, 100)
                    tipo = 'frutal'
                elif isinstance(item1.planta, Peral):
                    nueva_planta = Peral(0.5, 0, (pos_x, pos_y), 100, 100)
                    tipo = 'frutal'
                elif isinstance(item1.planta, Rosal):
                    nueva_planta = Rosal(0.3, 0, (pos_x, pos_y), 100, 100)
                    tipo = 'floral'
                elif isinstance(item1.planta, Orquidero):
                    nueva_planta = Orquidero(0.3, 0, (pos_x, pos_y), 100, 100)
                    tipo = 'floral'
                elif isinstance(item1.planta, Cempasuchil):
                    nueva_planta = Cempasuchil(0.3, 0, (pos_x, pos_y), 100, 100)
                    tipo = 'floral'

                if nueva_planta and tipo:
                    nuevas_plantas.append((nueva_planta, tipo))
                    # Mensaje
                    self.lbl_estado.setText(f"Estado: Nueva {nueva_planta.__class__.__name__} ha brotado!")
                    self.registrar_accion(
                        nueva_planta.__class__.__name__,
                        "Reproducción",
                        "Nueva planta ha brotado"
                    )

        # Agregar nuevas plantas al ecosistema
        for planta, tipo in nuevas_plantas:
            self.ecosistema.agregar_entidad(planta, tipo)
            especie = planta.__class__.__name__
            if especie in self.imagenes_plantas:
                item = PlantaGraphicsItem(planta, self.imagenes_plantas[especie])
                self.planta_items.append(item)

    def mostrar_estadisticas(self):
        """Actualiza y muestra las estadísticas del ecosistema"""
        conteo_especies = {}
        energia_promedio = {}

        for item in self.animal_items:
            if item.animal.estar_vivo:
                especie = item.animal.__class__.__name__
                conteo_especies[especie] = conteo_especies.get(especie, 0) + 1

                if especie not in energia_promedio:
                    energia_promedio[especie] = []
                energia_promedio[especie].append(item.animal.nivel_energia)

        # Calcular promedios de energía
        for especie in energia_promedio:
            energia_promedio[especie] = sum(energia_promedio[especie]) / len(energia_promedio[especie])

        # Actualizar etiquetas
        stats_text = "Población: "
        for especie, cantidad in conteo_especies.items():
            stats_text += f"{especie}: {cantidad} "
        self.lbl_poblacion.setText(stats_text)

    def verificar_directorio_imagenes(self):
        if not os.path.exists('imagenes'):
            try:
                os.makedirs('imagenes')
                QMessageBox.warning(self, "Aviso",
                                    "Se ha creado el directorio 'imagenes'. Por favor, agregue las imágenes de los animales.")
            except Exception as e:
                QMessageBox.critical(self, "Error",
                                     f"No se pudo crear el directorio de imágenes: {str(e)}")

    def registrar_accion(self, animal_tipo: str, accion: str, detalles: str = ""):
        """Registra una acción en el panel lateral"""
        timestamp = QTime.currentTime().toString("HH:mm:ss")
        accion_texto = f"[{timestamp}] {animal_tipo}: {accion}"
        if detalles:
            accion_texto += f" - {detalles}"

        self.lista_acciones.insertItem(0, accion_texto)

        # Mantener un límite de acciones mostradas
        while self.lista_acciones.count() > self.max_acciones:
            self.lista_acciones.takeItem(self.lista_acciones.count() - 1)

    def registrar_evento_planta(self, planta, accion, detalles=""):
        """Registra eventos específicos de las plantas"""
        timestamp = QTime.currentTime().toString("HH:mm:ss")
        tipo_planta = planta.__class__.__name__

        # Formatear mensaje según el tipo de acción
        if accion == "generar_frutos":
            mensaje = f"[{timestamp}] 🌳 {tipo_planta}: Generó {detalles} nuevos frutos"
        elif accion == "crecer":
            mensaje = f"[{timestamp}] 🌱 {tipo_planta}: Creció {detalles}m"
        elif accion == "absorber_agua":
            mensaje = f"[{timestamp}] 💧 {tipo_planta}: Absorbió {detalles} de agua"
        else:
            mensaje = f"[{timestamp}] {tipo_planta}: {accion} - {detalles}"

        self.lista_acciones.insertItem(0, mensaje)

        # Mantener un límite de acciones mostradas
        while self.lista_acciones.count() > self.max_acciones:
            self.lista_acciones.takeItem(self.lista_acciones.count() - 1)

    def setup_ui(self):
        try:
            # Widget central
            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            # Layout principal horizontal
            main_layout = QHBoxLayout(central_widget)

            # Layout para la parte principal (izquierda)
            left_layout = QVBoxLayout()

            self.btn_guardar = QPushButton("Guardar Estado")
            self.btn_cargar = QPushButton("Cargar Estado")

            # Panel superior con información
            info_panel = QHBoxLayout()
            self.lbl_poblacion = QLabel("Población total: 0")
            self.lbl_estado = QLabel("Estado: Esperando inicio")
            info_panel.addWidget(self.lbl_poblacion)
            info_panel.addWidget(self.lbl_estado)

            # Escena y vista
            self.scene = QGraphicsScene()
            self.view = QGraphicsView(self.scene)
            self.scene.setSceneRect(0, 0, self.ANCHO_ECOSISTEMA, self.ALTO_ECOSISTEMA)
            self.scene.setBackgroundBrush(QBrush(QColor("#90EE90")))

            # Panel de control
            control_panel = QHBoxLayout()
            self.btn_inicio = QPushButton("Iniciar Simulación")
            self.btn_inicio.clicked.connect(self.iniciar_simulacion)
            control_panel.addWidget(self.btn_inicio)

            # Agregar elementos al layout izquierdo
            left_layout.addLayout(info_panel)
            left_layout.addWidget(self.view)
            left_layout.addLayout(control_panel)

            # Crear un splitter para poder ajustar el tamaño del panel lateral
            splitter = QSplitter(Qt.Orientation.Horizontal)

            # Widget contenedor para la parte izquierda
            left_widget = QWidget()
            left_widget.setLayout(left_layout)

            # Agregar widgets al splitter
            splitter.addWidget(left_widget)

            # Configurar el panel lateral (derecha)
            right_widget = QWidget()
            right_layout = QVBoxLayout(right_widget)

            # Agregar botones al layout
            control_panel.addWidget(self.btn_guardar)
            control_panel.addWidget(self.btn_cargar)

            # Etiqueta para el panel lateral
            lbl_animales = QLabel("Animales Vivos")
            lbl_animales.setAlignment(Qt.AlignmentFlag.AlignCenter)
            right_layout.addWidget(lbl_animales)

            # Agregar la lista de animales
            right_layout.addWidget(self.lista_animales)

            # Separador
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setFrameShadow(QFrame.Shadow.Sunken)
            right_layout.addWidget(separator)

            # Panel de acciones
            lbl_acciones = QLabel("Registro de Acciones")
            lbl_acciones.setAlignment(Qt.AlignmentFlag.AlignCenter)
            right_layout.addWidget(lbl_acciones)
            right_layout.addWidget(self.lista_acciones)

            # Agregar el widget derecho al splitter
            splitter.addWidget(right_widget)

            # Establecer las proporciones del splitter
            splitter.setStretchFactor(0, 3)  # La parte principal ocupa más espacio
            splitter.setStretchFactor(1, 1)  # El panel lateral ocupa menos espacio

            # Agregar el splitter al layout principal
            main_layout.addWidget(splitter)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al configurar la interfaz: {str(e)}")
            self.close()

    def actualizar_lista_animales_y_plantas(self):
        """Actualiza la lista de animales vivos en el panel lateral"""
        self.lista_animales.clear()

        # Diccionario para agrupar animales por especie
        animales_por_especie = {}

        for item in self.animal_items:
            if item.animal.estar_vivo:
                especie = item.animal.__class__.__name__
                energia = item.animal.nivel_energia
                if especie not in animales_por_especie:
                    animales_por_especie[especie] = []
                animales_por_especie[especie].append(energia)

        # Agregar encabezado de animales
        self.lista_animales.addItem("====== ANIMALES ======")
        self.lista_animales.addItem("")

        # Agregar elementos a la lista agrupados por especie
        for especie, energias in animales_por_especie.items():
            # Agregar encabezado de especie
            self.lista_animales.addItem(f"=== {especie}s ({len(energias)}) ===")

            # Agregar cada animal con su energía
            for i, energia in enumerate(energias, 1):
                self.lista_animales.addItem(
                    f"  {especie} {i} - Energía: {energia:.1f}%"
                )

            # Agregar espacio entre especies
            self.lista_animales.addItem("")

        # Agregar separador
        self.lista_animales.addItem("====== PLANTAS ======")
        self.lista_animales.addItem("")

        # Diccionario para agrupar plantas por especie
        plantas_por_especie = {}
        for item in self.planta_items:
            if item.planta.estar_vivo:
                especie = item.planta.__class__.__name__
                if especie not in plantas_por_especie:
                    plantas_por_especie[especie] = []
                # Crear un diccionario con la información relevante de la planta
                info_planta = {
                    'altura': item.planta.altura,
                    'energia': item.planta.nivel_energia,
                    'agua': item.planta.nivel_agua
                }
                # Agregar información de frutos si es una planta frutal
                if hasattr(item.planta, 'frutos'):
                    info_planta['frutos'] = item.planta.frutos
                # Agregar información de flores si es una planta floral
                if hasattr(item.planta, 'flores'):
                    info_planta['flores'] = item.planta.flores

                plantas_por_especie[especie].append(info_planta)

        # Agregar elementos de plantas a la lista agrupados por especie
        for especie, plantas in plantas_por_especie.items():
            self.lista_animales.addItem(f"=== {especie}s ({len(plantas)}) ===")
            for i, info in enumerate(plantas, 1):
                self.lista_animales.addItem(
                    f"  {especie} {i} - Altura: {info['altura']:.1f}m"
                )
                # Mostrar frutos si es una planta frutal
                if 'frutos' in info:
                    self.lista_animales.addItem(
                        f"    Frutos: {info['frutos']}"
                    )
                # Mostrar flores si es una planta floral
                if 'flores' in info:
                    self.lista_animales.addItem(
                        f"    Flores: {info['flores']}"
                    )
                self.lista_animales.addItem(
                    f"    Agua: {info['agua']:.1f}% | Energía: {info['energia']:.1f}%"
                )
            self.lista_animales.addItem("")

    def iniciar_simulacion(self):
        try:
            # Crear nuevo ecosistema
            self.ecosistema = Ecosistema()

            # Deshabilitar el botón
            self.btn_inicio.setEnabled(False)
            self.btn_inicio.setText("Simulación en curso...")

            # Crear y agregar algunos animales de ejemplo
            self.crear_animales_iniciales()
            self.crear_plantas_iniciales()  # Agregar creación de plantas

            # Crear y configurar el timer
            if self.timer is None:
                self.timer = QTimer()
                self.timer.timeout.connect(self.actualizar_escena)
                self.timer.setInterval(100)

            # Iniciar el timer
            self.timer.start()

            # Actualizar estado
            self.lbl_estado.setText("Estado: Simulación en curso")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar simulación: {str(e)}")
            self.reiniciar_simulacion()

    def reanudar_simulacion(self):
        """Reanuda la simulación"""
        if self.ecosistema:
            self.ecosistema.reanudar_simulacion()
            if self.timer:
                self.timer.start()
            self.btn_pausar.setEnabled(True)
            self.btn_reanudar.setEnabled(False)
            self.lbl_estado.setText("Estado: Simulación en curso")

    def crear_animales_iniciales(self):
        try:
            # Limpiar animales anteriores
            self.animal_items.clear()

            def generar_posicion():
                return (
                    random.uniform(50, self.ANCHO_ECOSISTEMA - 50),
                    random.uniform(50, self.ALTO_ECOSISTEMA - 50)
                )

            # Crear instancias de animales con las ubicaciones
            animales = [
                (Leon("Leon", 100, 2.0, generar_posicion()), 'carnivoro'),
                (Leon("Leon", 100, 2.0, generar_posicion()), 'carnivoro'),
                (Aguila_real("Aguila", 100, 3.0, generar_posicion()), 'carnivoro'),
                (Aguila_real("Aguila", 100, 3.0, generar_posicion()), 'carnivoro'),
                (Conejo("Conejo", 100, 4.0, generar_posicion()), 'herbivoro'),
                (Conejo("Conejo", 100, 4.0, generar_posicion()), 'herbivoro'),
                (Conejo("Conejo", 100, 4.0, generar_posicion()), 'herbivoro'),
                (Ciervo("Ciervo", 100, 3.0, generar_posicion()), 'herbivoro'),
                (Ciervo("Ciervo", 100, 3.0, generar_posicion()), 'herbivoro'),
                (Ciervo("Ciervo", 100, 3.0, generar_posicion()), 'herbivoro')
            ]

            # Agregar cada animal al ecosistema y crear su representación gráfica
            for animal, tipo in animales:
                # Agregar al ecosistema
                self.ecosistema.agregar_entidad(animal, tipo)

                # Crear representación gráfica
                especie = animal.__class__.__name__
                if especie in self.imagenes_animales:
                    item = AnimalGraphicsItem(animal, self.imagenes_animales[especie])
                    self.animal_items.append(item)

        except Exception as e:
            raise Exception(f"Error al crear animales: {str(e)}")

    def actualizar_escena(self):
        try:
            self.scene.clear()

            # Verificar cazas antes del movimiento
            self.verificar_cazas()

            # Verificar alimentación de plantas antes del movimiento
            self.verificar_alimentacion_plantas()
            self.verificar_reproduccion_plantas()  # Añadir esta línea aquí


            # Lista para almacenar nuevos animales
            nuevos_animales = []

            # for item in self.planta_items:
            #     if item.planta.estar_vivo:
            #         pixmap_item = self.scene.addPixmap(item.pixmap)
            #         pixmap_item.setPos(item.x, item.y)
            #     else:
            #         self.planta_items.remove(item)

            for item in self.planta_items[:]:
                if item.planta.estar_vivo:
                    pixmap_item = self.scene.addPixmap(item.pixmap)
                    pixmap_item.setPos(item.x, item.y)
                    # Para registrar crecimiento
                    if item.planta.crecer():
                        self.registrar_evento_planta(
                            item.planta,
                            "crecer",
                            f"{item.planta.altura:.2f}"
                        )

                    # Para registrar generación de frutos (si es planta frutal)
                    if hasattr(item.planta, 'generar_frutos') and item.planta.generar_frutos():
                        self.registrar_evento_planta(
                            item.planta,
                            "generar_frutos",
                            str(item.planta.frutos)
                        )

                    # Para registrar absorción de agua
                    if item.planta.absorber_agua():
                        self.registrar_evento_planta(
                            item.planta,
                            "absorber_agua",
                            str(item.planta.nivel_agua)
                        )
                else:
                    self.planta_items.remove(item)

            # Mover animales y verificar reproducción
            for item in self.animal_items:
                if item.animal.estar_vivo:

                    # Registrar acciones especiales
                    if isinstance(item.animal, Volador) and random.random() < 0.1:
                        item.animal.volar()
                        self.registrar_accion(
                            item.animal.__class__.__name__,
                            "Volar",
                            "Voló por el ecosistema"
                        )

                    if isinstance(item.animal, Nadador) and random.random() < 0.1:
                        item.animal.nadar()
                        self.registrar_accion(
                            item.animal.__class__.__name__,
                            "Nadar",
                            "Nadó en el ecosistema"
                        )
                    # Mover animal
                    item.mover(self.ANCHO_ECOSISTEMA, self.ALTO_ECOSISTEMA)

                    # Intentar reproducción
                    otros_animales = [otro.animal for otro in self.animal_items
                                      if otro != item and otro.animal.estar_vivo]
                    nueva_cria = item.animal.reproducirse(otros_animales)

                    if nueva_cria:
                        # Determinar tipo
                        tipo = 'carnivoro' if isinstance(nueva_cria, (Leon, Aguila_real)) else 'herbivoro'
                        nuevos_animales.append((nueva_cria, tipo))
                        self.lbl_estado.setText(f"Estado: Nuevo {nueva_cria.__class__.__name__} ha nacido!")
                        self.registrar_accion(
                            item.animal.__class__.__name__,
                            "Reproducirse",
                            f"Dio nacimiento a un nuevo {nueva_cria.__class__.__name__}"
                        )

            # Agregar nuevos animales al ecosistema
            for animal, tipo in nuevos_animales:
                self.ecosistema.agregar_entidad(animal, tipo)
                if animal.__class__.__name__ in self.imagenes_animales:
                    item = AnimalGraphicsItem(animal, self.imagenes_animales[animal.__class__.__name__])
                    self.animal_items.append(item)

            # Dibujar animales y actualizar estadísticas
            self._actualizar_visualizacion()

        except Exception as e:
            print(f"Error al actualizar escena: {str(e)}")
            self.timer.stop()
            QMessageBox.critical(self, "Error",
                                 "Error al actualizar la simulación. La simulación se ha detenido.")
            self.reiniciar_simulacion()

    def _actualizar_visualizacion(self):
        """Actualiza la visualización de los animales y las estadísticas"""
        animales_vivos = {
            'carnivoros': 0,
            'herbivoros': 0
        }

        for item in self.animal_items[:]:
            if item.animal.estar_vivo:
                pixmap_item = self.scene.addPixmap(item.pixmap)
                pixmap_item.setPos(item.x, item.y)

                if isinstance(item.animal, (Leon, Aguila_real)):
                    animales_vivos['carnivoros'] += 1
                else:
                    animales_vivos['herbivoros'] += 1

        # Actualizar estadísticas
        self.mostrar_estadisticas()

        # Actualizar lista de animales y plantas
        self.actualizar_lista_animales_y_plantas()

        # Verificar balance del ecosistema
        self.verificar_balance_ecosistema(animales_vivos)

        self.view.viewport().update()

    def agregar_herbivoros_adicionales(self, cantidad: int):
        """Agrega nuevos herbívoros para mantener el equilibrio"""
        for _ in range(cantidad):
            pos_x = random.uniform(50, self.ANCHO_ECOSISTEMA - 50)
            pos_y = random.uniform(50, self.ALTO_ECOSISTEMA - 50)

            # Alternar entre conejos y ciervos
            if random.random() < 0.5:
                animal = Conejo("Conejo", 100, 4.0, (pos_x, pos_y))
            else:
                animal = Ciervo("Ciervo", 100, 3.0, (pos_x, pos_y))

            self.ecosistema.agregar_entidad(animal, 'herbivoro')
            item = AnimalGraphicsItem(animal, self.imagenes_animales[animal.__class__.__name__])
            self.animal_items.append(item)

    def registrar_alimentacion_herbivoro(self, herbivoro, planta, frutos_consumidos):
        """Registra cuando un herbívoro se alimenta de una planta"""
        timestamp = QTime.currentTime().toString("HH:mm:ss")
        mensaje = (f"[{timestamp}] 🍎 {herbivoro.__class__.__name__}: "
                   f"Consumió {frutos_consumidos} frutos de {planta.__class__.__name__}")

        self.lista_acciones.insertItem(0, mensaje)

        # Mantener un límite de acciones mostradas
        while self.lista_acciones.count() > self.max_acciones:
            self.lista_acciones.takeItem(self.lista_acciones.count() - 1)

    def verificar_balance_ecosistema(self, conteo: dict):
        """Verifica y mantiene el balance del ecosistema"""
        # Si hay muy pocos herbívoros comparado con carnívoros
        if (conteo['herbivoros'] < conteo['carnivoros'] * 2 and
                conteo['herbivoros'] < 5):
            # Agregar algunos herbívoros nuevos
            self.agregar_herbivoros_adicionales(3)

        # Si no quedan herbívoros, los carnívoros empiezan a perder energía más rápido
        if conteo['herbivoros'] == 0:
            for item in self.animal_items:
                if isinstance(item.animal, (Leon, Aguila_real)):
                    item.animal.nivel_energia = max(0, item.animal.nivel_energia - 1)

    def reiniciar_simulacion(self):
        if self.timer:
            self.timer.stop()
        if self.ecosistema:
            self.ecosistema.detener_simulacion()

        # Restablecer botones
        self.btn_inicio.setEnabled(True)
        self.btn_inicio.setText("Iniciar Simulación")
        self.btn_pausar.setEnabled(False)
        self.btn_reanudar.setEnabled(False)
        self.btn_reiniciar.setEnabled(False)

        # Limpiar elementos
        self.lbl_estado.setText("Estado: Esperando inicio")
        self.animal_items.clear()
        self.planta_items.clear()
        self.scene.clear()
        self.lista_animales.clear()
        self.lista_acciones.clear()

    def verificar_alimentacion_plantas(self):
        """Verifica si hay herbívoros que puedan alimentarse de plantas"""
        for animal_item in self.animal_items:
            if not animal_item.animal.estar_vivo or not isinstance(animal_item.animal, Herbivoro):
                continue

            # Si el animal tiene poca energía, buscar plantas
            if animal_item.animal.nivel_energia < 30:
                planta_cercana, distancia = animal_item.animal.buscar_planta_cercana(
                    [p.planta for p in self.planta_items],
                    animal_item.animal.ubicacion
                )

                if planta_cercana and distancia <= Herbivoro.DISTANCIA_ALIMENTACION:
                    frutos_antes = getattr(planta_cercana, 'frutos', 0)
                if animal_item.animal.alimentarse_de_planta(planta_cercana):
                    frutos_consumidos = frutos_antes - getattr(planta_cercana, 'frutos', 0)
                    self.registrar_alimentacion_herbivoro(
                        animal_item.animal,
                        planta_cercana,
                        frutos_consumidos
                    )

                    # Actualizar estado
                    self.lbl_estado.setText(
                        f"Estado: {animal_item.animal.__class__.__name__} "
                        f"consumió {frutos_consumidos} frutos de {planta_cercana.__class__.__name__}"
                    )

    def closeEvent(self, event):
        if self.ecosistema:
            self.ecosistema.detener_simulacion()
        if self.timer:
            self.timer.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = EcosistemaGUI()
    ventana.show()
    sys.exit(app.exec())