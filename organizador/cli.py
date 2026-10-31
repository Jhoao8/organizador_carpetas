import argparse
import logging
import sys
from collections import Counter
from pathlib import Path

from .configuracion import cargar_reglas
from .movedor import organizar
from .registro import configurar_log


def main():
    """Punto de entrada: lee la carpeta desde la terminal y la organiza."""
    parser = argparse.ArgumentParser(
        description="Organiza los archivos de una carpeta en subcarpetas por categoría."
    )
    parser.add_argument("carpeta", help="Ruta de la carpeta a organizar.")
    parser.add_argument(
        "--reglas",
        help="Ruta de un archivo JSON con reglas propias. "
        "Si no se indica, se usan las reglas por defecto.",
    )
    parser.add_argument(
        "--simular",
        action="store_true",
        help="Muestra qué se haría sin mover ningún archivo."
    )
    args = parser.parse_args()

    carpeta = Path(args.carpeta).resolve()
    if not carpeta.is_dir():
        print(f"Error: '{carpeta}' no existe o no es una carpeta.", file=sys.stderr)
        sys.exit(1)

    try:
        reglas = cargar_reglas(args.reglas)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    ruta_log = configurar_log()
    logger = logging.getLogger("organizador")
    logger.info(
        "INICIO: carpeta=%s simular=%s reglas=%s",
        carpeta, args.simular, args.reglas or "por defecto",
    )

    movimientos, errores = organizar(carpeta, reglas, simular=args.simular)

    logger.info(
        "FIN: %d archivos procesados, %d errores", len(movimientos), len(errores)
    )

    if not movimientos and not errores:
        print("No había archivos para organizar.")
        return

    if movimientos:
        if args.simular:
            print("SIMULACIÓN: no se movió ningún archivo.")
            for origen, destino in movimientos:
                print(f"{origen.name} -> {destino.relative_to(carpeta)}")

        por_categoria = Counter(destino.parent.name for _, destino in movimientos)
        for categoria, cantidad in por_categoria.items():
            print(f"{categoria}: {cantidad}")
        print(f"Total: {len(movimientos)}")

    if errores:
        print(
            f"Atención: {len(errores)} archivo(s) no se pudieron mover:",
            file=sys.stderr,
        )
        for archivo, motivo in errores:
            print(f"  {archivo.name}: {motivo}", file=sys.stderr)

    print(f"Registro: {ruta_log}")

    if errores:
        sys.exit(1)

if __name__ == "__main__":
    main()