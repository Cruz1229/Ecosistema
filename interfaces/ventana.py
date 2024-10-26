import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QLabel,
                             QToolBar, QPushButton, QHBoxLayout, QVBoxLayout,
                             QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap

class ObjetoEcosistema(QLabel):
    def __init__(self, imagen_path, x=0, y=0, parent=None):
        super().__init__(parent)

        # Cargar y escalar la imagen
        self.pixmap = QPixmap(imagen_path)
        self.pixmap = self.pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)

        # Establecer la imagen en el QLabel
        self.setPixmap(self.pixmap)

        # Permitir mover el objeto
        self.setMouseTracking(True)

        # Posición inicial
        self.move(x, y)

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

        layout_lateral = QVBoxLayout(barra_lateral)
        layout_lateral.setContentsMargins(10, 10, 10, 10)
        layout_lateral.setSpacing(10)

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
        layout_lateral.addWidget(btn_capibara)

        layout_lateral.addStretch()
        self.layout_principal.addWidget(barra_lateral)

    def crear_area_principal(self):
        self.area_ecosistema = AreaEcosistema()
        self.layout_principal.addWidget(self.area_ecosistema)

    def crear_capibara(self):
        # Crear una nueva instancia de capibara
        capibara = ObjetoEcosistema("capibara.png", 100, 100, self.area_ecosistema)
        capibara.show()

    def aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
        """)

    # [Métodos previos se mantienen igual]
    def detener_ecosistema(self):
        print("Ecosistema detenido")

    def reiniciar_ecosistema(self):
        print("Ecosistema reiniciado")

    def guardar_estado(self):
        print("Estado guardado")

    def cargar_estado(self):
        print("Estado cargado")

    def keyPressEvent(self, evento):
        if evento.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    sys.exit(app.exec())