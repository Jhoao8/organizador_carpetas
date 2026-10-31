import shutil
from pathlib import Path

from .clasificador import obtener_categoria


def organizar(carpeta, reglas):
    """Mueve los archivos de una carpeta a subcarpetas según su categoría.

    Recibe la carpeta y las reglas de clasificación, y devuelve un diccionario
    con la cantidad de archivos movidos por categoría.
    """
    carpeta = Path(carpeta)
    resumen = {}
    archivos = [ruta for ruta in carpeta.iterdir() if ruta.is_file()]

    for archivo in archivos:
        categoria = obtener_categoria(archivo.name, reglas)
        destino = carpeta / categoria
        archivo_destino = destino / archivo.name

        if archivo_destino.exists():
            continue

        destino.mkdir(exist_ok=True)
        shutil.move(archivo, archivo_destino)
        resumen[categoria] = resumen.get(categoria, 0) + 1

    return resumen