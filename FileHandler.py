from abc import ABC, abstractmethod


class FileReadingStrategy(ABC):
    """
    Clase abstracta que define la estrategia de lectura de archivos.
    Métodos:
    - read(path): Método abstracto que debe ser implementado por las clases hijas.
      Recibe como parámetro la ruta del archivo a leer.
    """

    @abstractmethod
    def read(self, path):
        pass


class FullReadStrategy(FileReadingStrategy):
    """
    Estrategia de lectura completa de archivos.
    Esta estrategia lee todo el contenido de un archivo dado su ruta.
    Args:
        path (str): La ruta del archivo a leer.
    Returns:
        str: El contenido completo del archivo.
    """

    def read(self, path):
        with open(path, "r") as file:
            return file.read()


class LineByLineReadStrategy(FileReadingStrategy):
    """
    Estrategia de lectura de archivos línea por línea.
    Esta estrategia lee un archivo línea por línea y devuelve una lista de las líneas leídas.
    Args:
        path (str): La ruta del archivo a leer.
    Returns:
        list: Una lista de las líneas leídas del archivo.
    """

    def read(self, path):
        lines = []
        with open(path, "r") as file:
            for line in file:
                lines.append(line)
        return lines


class FileHandler:
    """
    Clase que maneja la lectura de archivos.
    Lee el archivo utilizando la estrategia de lectura especificada.
    Args:
        path (str): Ruta del archivo a leer.
        strategy (FileReadingStrategy): Estrategia de lectura del archivo.
    Attributes:
        path (str): Ruta del archivo a leer.
        strategy (FileReadingStrategy): Estrategia de lectura del archivo.
    Methods:
        read(): Lee el archivo utilizando la estrategia de lectura
        especificada.
    Returns:
        str: Contenido del archivo leído.
    """

    def __init__(self, path, strategy: FileReadingStrategy):
        self.path = path
        self.strategy = strategy

    def read(self):
        return self.strategy.read(self.path)