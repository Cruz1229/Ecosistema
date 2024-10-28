import math

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QGraphicsScene, QGraphicsView,
                             QMessageBox, QLabel, QHBoxLayout)
from PyQt6.QtGui import QPixmap, QBrush, QPen, QColor
from PyQt6.QtCore import Qt, QTimer, QRectF
import sys
import os
import random
from typing import Dict, List
from Animales.Carnivoros.Carnivoro import Carnivoro
from Animales.Herbivoros.Herbivoro import Herbivoro
from Ecosistema import Ecosistema
from Animales.Animal import Animal
from Animales.Carnivoros.Leon import Leon
from Animales.Carnivoros.Aguila_real import Aguila_real
from Animales.Herbivoros.Conejo import Conejo
from Animales.Herbivoros.Ciervo import Ciervo
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
        self.TIEMPO_MINIMO_REPRODUCCION = 500  # Aumentado significativamente
        self.PROBABILIDAD_REPRODUCCION = 0.2  # 20% de probabilidad cuando se cumplan las condiciones
        self.ENERGIA_MINIMA_REPRODUCCION = 70  # Energía mínima necesaria para reproducirse
        self.COSTO_ENERGIA_REPRODUCCION = 30  # Energía que cuesta reproducirse

        # Contadores de tiempo específicos por especie
        self.TIEMPOS_REPRODUCCION = {
            'Leon': 700,         # Más tiempo para carnívoros grandes
            'Aguila_real': 600,
            'Conejo': 400,       # Menor tiempo para herbívoros pequeños
            'Ciervo': 500
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

        # Representaciones gráficas de los animales
        self.animal_items = []

        # Timer para actualizar la visualización
        self.timer = None

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

        # Parámetros para plantas
        self.TIEMPO_MINIMO_REPRODUCCION_PLANTAS = 800
        self.PROBABILIDAD_REPRODUCCION_PLANTAS = 0.1
        self.DISTANCIA_REPRODUCCION_PLANTAS = 100

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

    def realizar_caza(self, depredador: Animal, presa: Animal):
        """Procesa el intento de caza"""
        # Intentar cazar
        if depredador.cazar(presa):
            # Si la caza fue exitosa, alimentarse
            if depredador.alimentarse(presa):
                self.lbl_estado.setText(
                    f"Estado: {depredador.__class__.__name__} cazó y se alimentó de {presa.__class__.__name__}"
                )
        else:
            # Caza fallida
            self.lbl_estado.setText(
                f"Estado: {depredador.__class__.__name__} falló la caza"
            )
            # Hacer que la presa huya
            self.hacer_huir_presa(presa)

    def hacer_huir_presa(self, presa: AnimalGraphicsItem):
        """Hace que la presa huya cuando la caza falla"""
        # Implementar el método huir si existe en la clase Herbívoro
        if isinstance(presa.animal, Herbivoro):
            presa.animal.huir()

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

    def setup_ui(self):
        try:
            # Widget central
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)

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

            # Agregar todo al layout principal
            layout.addLayout(info_panel)
            layout.addWidget(self.view)
            layout.addLayout(control_panel)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al configurar la interfaz: {str(e)}")
            self.close()

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

            for item in self.planta_items[:]:
                if item.planta.estar_vivo:
                    pixmap_item = self.scene.addPixmap(item.pixmap)
                    pixmap_item.setPos(item.x, item.y)
                else:
                    self.planta_items.remove(item)

            # Mover animales
            for item in self.animal_items:
                if item.animal.estar_vivo:
                    item.mover(self.ANCHO_ECOSISTEMA, self.ALTO_ECOSISTEMA)

            # Verificar reproducción
            self.verificar_reproduccion()

            # Dibujar animales y actualizar estadísticas
            animales_vivos = {
                'carnivoros': 0,
                'herbivoros': 0
            }

            for item in self.animal_items[:]:
                if item.animal.estar_vivo:
                    pixmap_item = self.scene.addPixmap(item.pixmap)
                    pixmap_item.setPos(item.x, item.y)

                    # Contar por tipo
                    if isinstance(item.animal, (Leon, Aguila_real)):
                        animales_vivos['carnivoros'] += 1
                    else:
                        animales_vivos['herbivoros'] += 1
                else:
                    self.animal_items.remove(item)

            # Actualizar estadísticas
            self.mostrar_estadisticas()

            # Verificar balance del ecosistema
            self.verificar_balance_ecosistema(animales_vivos)

            self.view.viewport().update()

        except Exception as e:
            print(f"Error al actualizar escena: {str(e)}")
            self.timer.stop()
            QMessageBox.critical(self, "Error",
                                 "Error al actualizar la simulación. La simulación se ha detenido.")
            self.reiniciar_simulacion()

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
        self.btn_inicio.setEnabled(True)
        self.btn_inicio.setText("Iniciar Simulación")
        self.lbl_estado.setText("Estado: Esperando inicio")
        self.animal_items.clear()
        self.planta_items.clear()  # Agregar limpieza de plantas
        self.scene.clear()

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