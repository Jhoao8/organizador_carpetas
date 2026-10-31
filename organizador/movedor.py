import shutil
from pathlib import Path

from .clasificador import obtener_categoria


def _ruta_sin_conflicto(ruta):
    """Devuelve una ruta libre: si ya existe, agrega ' (1)', ' (2)'... antes de la extensión."""
    contador = 1
    nueva_ruta = ruta
    while nueva_ruta.exists():
        nueva_ruta = ruta.with_name(f"{ruta.stem} ({contador}){ruta.suffix}")
        contador += 1
    return nueva_ruta

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

        destino.mkdir(exist_ok=True)
        archivo_destino = _ruta_sin_conflicto(destino / archivo.name)
        shutil.move(archivo, archivo_destino)
        resumen[categoria] = resumen.get(categoria, 0) + 1

    return resumen