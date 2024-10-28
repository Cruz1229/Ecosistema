import os
import pickle
from datetime import datetime

class GestorEstado:
    def __init__(self, directorio='estados'):
        self.directorio = directorio
        os.makedirs(directorio, exist_ok=True)

    def guardar_estado(self, estado):
        """Guarda el estado actual en un archivo"""
        nombre_archivo = f"estado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        ruta_archivo = os.path.join(self.directorio, nombre_archivo)

        with open(ruta_archivo, 'wb') as archivo:
            pickle.dump(estado, archivo)

        return ruta_archivo

    def cargar_estado(self, ruta_archivo):
        """Carga un estado desde un archivo"""
        try:
            with open(ruta_archivo, 'rb') as archivo:
                estado = pickle.load(archivo)
            return estado
        except FileNotFoundError:
            return None

    def listar_estados(self):
        """Retorna una lista de los archivos de estado disponibles"""
        return [archivo for archivo in os.listdir(self.directorio) if archivo.endswith('.pkl')]

    def obtener_info_estado(self, archivo):
        """Obtiene información básica de un archivo de estado"""
        ruta_archivo = os.path.join(self.directorio, archivo)
        tamano = os.path.getsize(ruta_archivo)
        fecha = datetime.fromtimestamp(os.path.getmtime(ruta_archivo)).strftime('%Y-%m-%d %H:%M:%S')
        return {'nombre': archivo, 'tamano': tamano, 'fecha': fecha}