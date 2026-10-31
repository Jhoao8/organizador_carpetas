import logging
from pathlib import Path

RUTA_LOG = Path.home() / ".organizador" / "organizador.log"


def configurar_log(ruta=RUTA_LOG):
    """Configura el registro del programa en un archivo y devuelve su ruta."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("organizador")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        manejador = logging.FileHandler(ruta, encoding="utf-8")
        manejador.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(manejador)

    return ruta