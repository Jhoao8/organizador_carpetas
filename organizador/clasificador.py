from pathlib import Path


def obtener_categoria(nombre_archivo, reglas):
    """Devuelve la categoría de un archivo según las reglas recibidas.

    Recibe el nombre del archivo y un diccionario categoría -> extensiones.
    Si ninguna categoría coincide, devuelve "Otros".
    """
    extension = Path(nombre_archivo).suffix.lower()
    for categoria, extensiones in reglas.items():
        if extension in extensiones:
            return categoria
    return "Otros"