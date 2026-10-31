import json
from pathlib import Path

RUTA_POR_DEFECTO = Path(__file__).parent / "reglas_por_defecto.json"


def cargar_reglas(ruta=None):
    """Carga las reglas de clasificación desde un archivo JSON."""
    ruta = Path(ruta or RUTA_POR_DEFECTO)

    try:
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        raise ValueError(f"No se encontró el archivo de reglas: {ruta}") from None
    except json.JSONDecodeError as error:
        raise ValueError(f"El archivo '{ruta}' no es un JSON válido: {error}") from None

    if not isinstance(datos, dict):
        raise ValueError("El archivo de reglas debe contener un objeto con categorías.")

    reglas = {}
    for categoria, extensiones in datos.items():
        if not isinstance(extensiones, list):
            raise ValueError(
                f"La categoria '{categoria}' debe tener una lista de extensiones."
            )
        if not all(isinstance(e, str) and e.startswith(".") for e in extensiones):
            raise ValueError(
                f"Las extensiones de '{categoria}' deben ser textos que empiecen con punto."
            )
        reglas[categoria] = tuple(e.lower() for e in extensiones)

    return reglas