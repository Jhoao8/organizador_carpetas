import logging
import shutil
from pathlib import Path

from .clasificador import obtener_categoria

logger = logging.getLogger("organizador")

EXTENSIONES_TEMPORALES = (".crdownload", ".part", ".partial", ".tmp", ".download")
NOMBRES_IGNORADOS = ("desktop.ini", "thumbs.db")


def _debe_ignorarse(archivo):
    """Indica si un archivo es temporal o del sistema y no debe moverse."""
    return (
        archivo.suffix.lower() in EXTENSIONES_TEMPORALES
        or archivo.name.lower() in NOMBRES_IGNORADOS
    )


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
    nada, solo calcula los movimientos. Ignora archivos temporales y del sistema.
    Devuelve (movimientos, errores): una lista de tuplas (origen, destino) y
    una lista de tuplas (archivo, motivo) con los que no se pudieron mover.
    """
    carpeta = Path(carpeta)
    movimientos = []
    errores = []
    archivos = [
        ruta
        for ruta in carpeta.iterdir()
        if ruta.is_file() and not _debe_ignorarse(ruta)
    ]

    for archivo in archivos:
        categoria = obtener_categoria(archivo.name, reglas)
        destino = carpeta / categoria
        archivo_destino = _ruta_sin_conflicto(destino / archivo.name)

        if simular:
            logger.info("SIMULADO: %s -> %s", archivo, archivo_destino)
        else:
            try:
                destino.mkdir(exist_ok=True)
                shutil.move(archivo, archivo_destino)
            except OSError as error:
                logger.error("ERROR al mover %s: %s", archivo, error)
                errores.append((archivo, error.strerror or str(error)))
                continue
            logger.info("MOVIDO: %s -> %s", archivo, archivo_destino)

        movimientos.append((archivo, archivo_destino))

    return movimientos, errores