import os
import pickle
from datetime import datetime

class GestorEstado:
    """Gestor para guardar y cargar estados del ecosistema.

    Esta clase proporciona funcionalidades para persistir y recuperar estados
    del ecosistema, permitiendo guardar el progreso y restaurarlo posteriormente.

    Attributes:
        directorio (str): Ruta del directorio donde se almacenarán los estados.
    """

    def __init__(self, directorio='estados'):
        """Inicializa el gestor de estados.

        Args:
            directorio (str, opcional): Ruta donde se guardarán los estados.
                Defaults to 'estados'.
        """
        self.directorio = directorio
        os.makedirs(directorio, exist_ok=True)

    def guardar_estado(self, estado):
        """Guarda el estado actual del ecosistema en un archivo.

        Serializa el estado actual y lo guarda en un archivo con timestamp
        en el nombre para identificarlo unívocamente.

        Args:
            estado (object): Estado del ecosistema a guardar.

        Returns:
            str: Ruta completa del archivo donde se guardó el estado.

        Example:
            >>> gestor = GestorEstado()
            >>> ruta = gestor.guardar_estado(mi_ecosistema)
            >>> print(f"Estado guardado en: {ruta}")
        """
        nombre_archivo = f"estado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        ruta_archivo = os.path.join(self.directorio, nombre_archivo)

        with open(ruta_archivo, 'wb') as archivo:
            pickle.dump(estado, archivo)

        return ruta_archivo

    def cargar_estado(self, ruta_archivo):
        """Carga un estado previo desde un archivo.

        Args:
            ruta_archivo (str): Ruta del archivo que contiene el estado a cargar.

        Returns:
            object: Estado cargado del archivo, o None si el archivo no existe.

        Raises:
            FileNotFoundError: Si el archivo especificado no existe.

        Example:
            >>> gestor = GestorEstado()
            >>> estado = gestor.cargar_estado("estados/mi_estado.pkl")
            >>> if estado:
            ...     print("Estado cargado exitosamente")
        """
        try:
            with open(ruta_archivo, 'rb') as archivo:
                estado = pickle.load(archivo)
            return estado
        except FileNotFoundError:
            return None

    def listar_estados(self):
        """Obtiene la lista de archivos de estado disponibles.

        Returns:
            list[str]: Lista de nombres de archivos de estado (.pkl) en el directorio.

        Example:
            >>> gestor = GestorEstado()
            >>> estados = gestor.listar_estados()
            >>> for estado in estados:
            ...     print(estado)
        """
        return [archivo for archivo in os.listdir(self.directorio) if archivo.endswith('.pkl')]

    def obtener_info_estado(self, archivo):
        """Obtiene información detallada de un archivo de estado.

        Recopila metadatos sobre un archivo de estado específico, incluyendo
        su nombre, tamaño y fecha de modificación.

        Args:
            archivo (str): Nombre del archivo de estado.

        Returns:
            dict: Diccionario con la información del archivo:
                - nombre (str): Nombre del archivo
                - tamano (int): Tamaño en bytes
                - fecha (str): Fecha de modificación en formato 'YYYY-MM-DD HH:MM:SS'

        Example:
            >>> gestor = GestorEstado()
            >>> info = gestor.obtener_info_estado("estado_20240228_120000.pkl")
            >>> print(f"Tamaño: {info['tamano']} bytes")
            >>> print(f"Fecha: {info['fecha']}")
        """
        ruta_archivo = os.path.join(self.directorio, archivo)
        tamano = os.path.getsize(ruta_archivo)
        fecha = datetime.fromtimestamp(os.path.getmtime(ruta_archivo)).strftime('%Y-%m-%d %H:%M:%S')
        return {'nombre': archivo, 'tamano': tamano, 'fecha': fecha}