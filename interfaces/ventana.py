import os
import sys
from random import random, randint

from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QLabel,
                             QToolBar, QPushButton, QHBoxLayout, QVBoxLayout,
                             QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QPixmap
from Animales.Herbivoros.Capibara import Capibara
import pickle  # Agregar al inicio del archivo

# Constante para la ruta de imágenes
RUTA_IMAGENES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes")

class ObjetoEcosistema(QLabel):
    def __init__(self, imagen_path, x=0, y=0, parent=None, tipo_organismo=None):
        super().__init__(parent)

    # Crear instancia del modelo
        if tipo_organismo == "capibara":
            self.modelo = Capibara(
                especie="Capibara perron",
                nivelEnergia=100,
                velocidad=20,
                ubicacion=(x, y)
            )


        # Inicializar el timer para movimiento aleatorio
        self.timer_movimiento = QTimer(self)
        self.timer_movimiento.timeout.connect(self.mover_aleatoriamente)
        self.timer_movimiento.start(1000)  # Actualizar cada 1000ms (1 segundo)

        # Verificar si la imagen existe
        if not os.path.exists(imagen_path):
            print(f"Error: No se encuentra la imagen en {imagen_path}")
            return

        # Cargar y escalar la imagen
        self.pixmap = QPixmap(imagen_path)
        if self.pixmap.isNull():
            print(f"Error: No se pudo cargar la imagen {imagen_path}")
            return

        self.pixmap = self.pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        # Establecer la imagen en el QLabel
        self.setPixmap(self.pixmap)

        # Permitir mover el objeto
        self.setMouseTracking(True)

        # Posición inicial
        self.move(x, y)

    def mover_aleatoriamente(self):
        try:
            if not hasattr(self, 'modelo') or not self.parent():
                return

            # Obtener los límites del área de movimiento
            area_padre = self.parent().size()
            max_x = area_padre.width() - self.width()
            max_y = area_padre.height() - self.height()

            # Posición actual
            pos_actual = self.pos()

            # Generar un movimiento aleatorio entre -50 y 50 píxeles en cada dirección
            delta_x = randint(-50, 50)
            delta_y = randint(-50, 50)

            # Calcular nueva posición
            nueva_x = max(0, min(max_x, pos_actual.x() + delta_x))
            nueva_y = max(0, min(max_y, pos_actual.y() + delta_y))

            # Mover el capibara
            self.move(nueva_x, nueva_y)

            # Actualizar la ubicación en el modelo
            self.modelo.ubicacion = (nueva_x, nueva_y)

            # Reducir energía al moverse
            nueva_energia = max(0, self.modelo.nivel_energia - 2)
            self.modelo.nivel_energia = nueva_energia

            # Imprimir estado actual (debug)
            print(f"Energía: {self.modelo.nivel_energia}")

            # Detener movimiento si no hay energía
            if self.modelo.nivel_energia <= 0:
                print("¡Sin energía! El capibara se detiene.")
                self.timer_movimiento.stop()

        except Exception as e:
            print(f"Error en mover_aleatoriamente: {str(e)}")
            import traceback
            traceback.print_exc()


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            if event.buttons() & Qt.MouseButton.LeftButton:
                delta = event.pos() - self.drag_start_position
                self.move(self.pos() + delta)

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            del self.drag_start_position

class AreaEcosistema(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QFrame { background-color: #ecf0f1; }")
        self.setAcceptDrops(True)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.capibaras = []  # Inicializar la lista aquí
        self.btn_reproducir = None  # Para mantener referencia al botón de reproducción
        self.layout_lateral = None  # Agregar esta línea
        self.capibaras_llegados = 0  # Agregar esta línea
        self.ecosistema_pausado = False  # Nuevo estado para controlar la pausa
        self.inicializarUI()

    def inicializarUI(self):
        # Configuración básica de la ventana
        self.setWindowTitle("Simulador de Ecosistema")
        self.showFullScreen()

        # Widget central y layout principal
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_principal = QHBoxLayout(self.widget_central)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # Crear componentes principales
        self.crear_barra_herramientas()
        self.crear_barra_lateral()
        self.crear_area_principal()

        # Aplicar estilos
        self.aplicar_estilos()

    def crear_barra_herramientas(self):
        # [Código previo de la barra de herramientas se mantiene igual]
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet("QToolBar { background-color: #2c3e50; spacing: 10px; padding: 5px; }")
        self.addToolBar(toolbar)

        botones = [
            ("Detener ecosistema", self.detener_ecosistema),
            ("Reiniciar ecosistema", self.reiniciar_ecosistema),
            ("Guardar Estado", self.guardar_estado),
            ("Cargar estado", self.cargar_estado)
        ]

        for texto, funcion in botones:
            btn = QPushButton(texto)
            btn.setMinimumHeight(40)
            if texto == "Detener ecosistema":
                self.btn_detener = btn
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 5px 15px;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 2px 5px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #216a9c;
                }
            """)
            btn.clicked.connect(funcion)
            toolbar.addWidget(btn)

    def crear_barra_lateral(self):
        barra_lateral = QFrame()
        barra_lateral.setMinimumWidth(200)
        barra_lateral.setMaximumWidth(200)
        barra_lateral.setStyleSheet("QFrame { background-color: #34495e; }")

        self.layout_lateral = QVBoxLayout(barra_lateral)  # Guardar referencia al layout
        self.layout_lateral.setContentsMargins(10, 10, 10, 10)
        self.layout_lateral.setSpacing(10)

        # Botón para crear capibara
        btn_capibara = QPushButton("Crear Capibara")
        btn_capibara.clicked.connect(self.crear_capibara)
        btn_capibara.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 5px 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #243342;
            }
            QPushButton:pressed {
                background-color: #1a242f;
            }
        """)
        self.layout_lateral.addWidget(btn_capibara)

        self.layout_lateral.addStretch()
        self.layout_principal.addWidget(barra_lateral)

    def crear_area_principal(self):
        self.area_ecosistema = AreaEcosistema()
        self.layout_principal.addWidget(self.area_ecosistema)

    def crear_capibara(self):
        try:
            # Construir la ruta completa a la imagen
            ruta_imagen = os.path.join(RUTA_IMAGENES, "capibara.png")

            print(f"Intentando cargar imagen desde: {ruta_imagen}")  # Debug

            # Verificar si el directorio existe
            if not os.path.exists(RUTA_IMAGENES):
                print(f"Error: El directorio de imágenes no existe: {RUTA_IMAGENES}")
                return

            # Verificar si la imagen existe
            if not os.path.exists(ruta_imagen):
                print(f"Error: La imagen no existe en: {ruta_imagen}")
                return

            # Crear una nueva instancia de capibara con posición aleatoria
            x = randint(100, self.area_ecosistema.width() - 100)
            y = randint(100, self.area_ecosistema.height() - 100)

            capibara = ObjetoEcosistema(
                imagen_path=ruta_imagen,
                x=x,
                y=y,
                parent=self.area_ecosistema,
                tipo_organismo="capibara"
            )

            if self.ecosistema_pausado and hasattr(capibara, 'timer_movimiento'):
                capibara.timer_movimiento.stop()

            # Agregar el capibara a la lista
            self.capibaras.append(capibara)

            # Mostrar el capibara
            capibara.show()

            if hasattr(capibara, 'modelo'):
                print(f"Capibara #{len(self.capibaras)} creado exitosamente")
                print(f"Especie: {capibara.modelo.especie}")
                print(f"Ubicación: {capibara.modelo.ubicacion}")
                print(f"Nivel de energía: {capibara.modelo.nivel_energia}")

                # Actualizar los botones laterales después de crear el capibara
                self.actualizar_botones_laterales()  # Agregar esta línea
            else:
                print("No se pudo crear el modelo de capibara")

        except Exception as e:
            print(f"Error al crear capibara: {str(e)}")
            import traceback
            traceback.print_exc()


    def actualizar_botones_laterales(self):
        # Si hay 2 o más capibaras y el botón no existe
        if len(self.capibaras) >= 2 and self.btn_reproducir is None:
            self.btn_reproducir = QPushButton("Reproducirse")
            self.btn_reproducir.clicked.connect(self.reproducir_capibaras)
            self.btn_reproducir.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 5px 15px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 4px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #219a52;
                }
                QPushButton:pressed {
                    background-color: #1e8449;
                }
            """)
            # Insertar el botón antes del stretch
            self.layout_lateral.insertWidget(self.layout_lateral.count() - 1, self.btn_reproducir)

        # Si hay menos de 2 capibaras y el botón existe
        elif len(self.capibaras) < 2 and self.btn_reproducir is not None:
            self.btn_reproducir.deleteLater()
            self.btn_reproducir = None

    def reproducir_capibaras(self):
        print("Iniciando reproducción de capibaras...")
        if len(self.capibaras) < 2:
            return

        capibara1 = self.capibaras[0]
        capibara2 = self.capibaras[1]

        # Verificar que tienen suficiente energía
        if capibara1.modelo.nivel_energia < 30 or capibara2.modelo.nivel_energia < 30:
            print("Los capibaras no tienen suficiente energía para reproducirse")
            return

        pos1 = capibara1.pos()
        pos2 = capibara2.pos()
        punto_encuentro = ((pos1.x() + pos2.x()) // 2, (pos1.y() + pos2.y()) // 2)

        # Reiniciar el contador
        self.capibaras_llegados = 0
        print("Iniciando movimiento de capibaras hacia el punto de encuentro")

        self.mover_capibara_a_punto(capibara1, punto_encuentro)
        self.mover_capibara_a_punto(capibara2, punto_encuentro)

    def mover_capibara_a_punto(self, capibara, punto):
        print(f"Moviendo capibara hacia punto ({punto[0]}, {punto[1]})")
        capibara.timer_movimiento.stop()
        timer = QTimer(self)
        pasos = 0
        max_pasos = 20

        def mover_paso():
            nonlocal pasos
            if pasos >= max_pasos:
                timer.stop()
                capibara.timer_movimiento.start()
                self.capibaras_llegados += 1
                print(f"Capibara llegó al punto. Total llegados: {self.capibaras_llegados}")

                if self.capibaras_llegados >= 2:
                    print("Ambos capibaras en posición, creando cría...")
                    try:
                        self.crear_cria(punto[0], punto[1])
                    except Exception as e:
                        print(f"Error al crear cría: {str(e)}")
                    self.capibaras_llegados = 0
                return

            # Calcular el porcentaje del camino recorrido
            progreso = pasos / max_pasos
            # Interpolar linealmente entre la posición actual y el destino
            pos_actual = capibara.pos()
            nuevo_x = pos_actual.x() + (punto[0] - pos_actual.x()) * 0.1
            nuevo_y = pos_actual.y() + (punto[1] - pos_actual.y()) * 0.1

            # Mover el capibara
            capibara.move(int(nuevo_x), int(nuevo_y))
            pasos += 1

        timer.timeout.connect(mover_paso)
        timer.start(50)

    def crear_cria(self, x, y):
        try:
            ruta_imagen = os.path.join(RUTA_IMAGENES, "capibara.png")
            print(f"Intentando crear cría en posición ({x}, {y})")

            if not os.path.exists(ruta_imagen):
                print(f"Error: No se encuentra la imagen en {ruta_imagen}")
                return

            # Crear nueva cría con una pequeña variación en la posición
            offset_x = randint(-20, 20)
            offset_y = randint(-20, 20)

            cria = ObjetoEcosistema(
                imagen_path=ruta_imagen,
                x=x + offset_x,
                y=y + offset_y,
                parent=self.area_ecosistema,
                tipo_organismo="capibara"
            )

            # Hacer la cría más pequeña
            pixmap_original = QPixmap(ruta_imagen)
            pixmap_escalado = pixmap_original.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
            cria.setPixmap(pixmap_escalado)

            # Agregar la cría a la lista y mostrarla
            self.capibaras.append(cria)
            cria.show()

            print(f"Cría creada exitosamente en ({x + offset_x}, {y + offset_y})")
            print(f"Total de capibaras ahora: {len(self.capibaras)}")

            # Reducir energía de los padres
            self.capibaras[0].modelo.nivel_energia -= 20
            self.capibaras[1].modelo.nivel_energia -= 20

            # Actualizar botones
            self.actualizar_botones_laterales()

        except Exception as e:
            print(f"Error detallado al crear cría: {str(e)}")
            import traceback
            traceback.print_exc()

    def aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
        """)

    # [Métodos previos se mantienen igual]
    def detener_ecosistema(self):
        try:
            self.ecosistema_pausado = not self.ecosistema_pausado  # Alternar estado

        # Actualizar todos los capibaras
            for capibara in self.capibaras:
                if hasattr(capibara, 'timer_movimiento'):
                    if self.ecosistema_pausado:
                        capibara.timer_movimiento.stop()
                    else:
                        capibara.timer_movimiento.start()

        # Actualizar el texto del botón
            if self.ecosistema_pausado:
                self.btn_detener.setText("Reanudar ecosistema")
                self.btn_detener.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        padding: 5px 15px;
                        font-size: 14px;
                        font-weight: bold;
                        margin: 2px 5px;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                    QPushButton:pressed {
                        background-color: #a93226;
                    }
                    """)
            else:
                self.btn_detener.setText("Detener ecosistema")
                self.btn_detener.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        padding: 5px 15px;
                        font-size: 14px;
                        font-weight: bold;
                        margin: 2px 5px;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                    QPushButton:pressed {
                        background-color: #216a9c;
                    }
                """)
            print("Ecosistema " + ("pausado" if self.ecosistema_pausado else "reanudado"))

        except Exception as e:
            print(f"Error al detener/reanudar el ecosistema: {str(e)}")
            import traceback
            traceback.print_exc()

    def reiniciar_ecosistema(self):
        try:
            # Primero detener todos los timers y desconectar señales
            for capibara in self.capibaras:
                if hasattr(capibara, 'timer_movimiento'):
                    capibara.timer_movimiento.stop()
                    capibara.timer_movimiento.deleteLater()

                # Asegurarse de que el capibara está desconectado de su parent
                if capibara.parent():
                    capibara.setParent(None)

                # Marcar para eliminación
                capibara.deleteLater()

            # Limpiar la lista de capibaras
            self.capibaras.clear()

            # Reiniciar el contador de capibaras llegados
            self.capibaras_llegados = 0

            # Eliminar el botón de reproducción si existe
            if self.btn_reproducir is not None:
                self.btn_reproducir.setParent(None)
                self.btn_reproducir.deleteLater()
                self.btn_reproducir = None

            # Forzar procesamiento de eventos pendientes
            QApplication.processEvents()

            # Forzar actualización del área del ecosistema
            self.area_ecosistema.update()

            print("Ecosistema reiniciado exitosamente")

        except Exception as e:
            print(f"Error al reiniciar el ecosistema: {str(e)}")
            import traceback
            traceback.print_exc()

    def guardar_estado(self):
        try:
            # Crear una lista con la información relevante de cada capibara
            estado_capibaras = []
            for capibara in self.capibaras:
                info_capibara = {
                'posicion': capibara.pos(),
                'especie': capibara.modelo.especie,
                'nivel_energia': capibara.modelo.nivel_energia,
                'velocidad': capibara.modelo.velocidad,
                'es_cria': capibara.size().width() == 30  # Para identificar si es una cría
                }
                estado_capibaras.append(info_capibara)

            # Guardar en un archivo
            with open('estado_ecosistema.pkl', 'wb') as archivo:
                pickle.dump(estado_capibaras, archivo)

            print("Estado guardado exitosamente")

        except Exception as e:
            print(f"Error al guardar estado: {str(e)}")
            import traceback
            traceback.print_exc()

    def cargar_estado(self):
        try:
            # Primero limpiar el ecosistema actual
            self.reiniciar_ecosistema()

            # Cargar el estado desde el archivo
            with open('estado_ecosistema.pkl', 'rb') as archivo:
                estado_capibaras = pickle.load(archivo)

        # Recrear cada capibara con su estado
            for info_capibara in estado_capibaras:
                ruta_imagen = os.path.join(RUTA_IMAGENES, "capibara.png")
                capibara = ObjetoEcosistema(
                    imagen_path=ruta_imagen,
                    x=info_capibara['posicion'].x(),
                    y=info_capibara['posicion'].y(),
                    parent=self.area_ecosistema,
                    tipo_organismo="capibara"
                )

                # Restaurar propiedades del modelo
                capibara.modelo.especie = info_capibara['especie']
                capibara.modelo.nivel_energia = info_capibara['nivel_energia']
                capibara.modelo.velocidad = info_capibara['velocidad']

                # Si era una cría, ajustar el tamaño
                if info_capibara['es_cria']:
                    pixmap_original = QPixmap(ruta_imagen)
                    pixmap_escalado = pixmap_original.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
                    capibara.setPixmap(pixmap_escalado)

                # Agregar a la lista y mostrar
                self.capibaras.append(capibara)
                capibara.show()

                # Si el ecosistema está pausado, detener el timer
                if self.ecosistema_pausado and hasattr(capibara, 'timer_movimiento'):
                    capibara.timer_movimiento.stop()

            # Actualizar botones laterales
            self.actualizar_botones_laterales()

            print("Estado cargado exitosamente")
            print(f"Capibaras restaurados: {len(self.capibaras)}")

        except FileNotFoundError:
            print("No se encontró archivo de estado guardado")
        except Exception as e:
            print(f"Error al cargar estado: {str(e)}")
            import traceback
            traceback.print_exc()

    def keyPressEvent(self, evento):
        if evento.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    sys.exit(app.exec())