import logging
import shutil
from pathlib import Path

from .clasificador import obtener_categoria

logger = logging.getLogger("organizador")


def _ruta_sin_conflicto(ruta):
    """Devuelve una ruta libre: si ya existe, agrega ' (1)', ' (2)'... antes de la extensión."""
    contador = 1
    nueva_ruta = ruta
    while nueva_ruta.exists():
        nueva_ruta = ruta.with_name(f"{ruta.stem} ({contador}){ruta.suffix}")
        contador += 1
    return nueva_ruta

def organizar(carpeta, reglas, simular=False):
    """Mueve los archivos de una carpeta a subcarpetas según su categoría.

    Recibe la carpeta y las reglas de clasificación. Con simular=True no mueve
    nada, solo calcula los movimientos. Devuelve una lista de tuplas
    (origen, destino) con cada movimiento realizado o simulado.
    """
    carpeta = Path(carpeta)
    movimientos = []
    archivos = [ruta for ruta in carpeta.iterdir() if ruta.is_file()]

    for archivo in archivos:
        categoria = obtener_categoria(archivo.name, reglas)
        destino = carpeta / categoria
        archivo_destino = _ruta_sin_conflicto(destino / archivo.name)

        if not simular:
            destino.mkdir(exist_ok=True)
            shutil.move(archivo, archivo_destino)
            logger.info("MOVIDO: %s -> %s", archivo, archivo_destino)
        else:
            logger.info("SIMULADO: %s -> %s", archivo, archivo_destino)

        movimientos.append((archivo, archivo_destino))

    return movimientos