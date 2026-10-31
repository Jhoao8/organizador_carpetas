import argparse
import sys
from collections import Counter
from pathlib import Path

from .configuracion import cargar_reglas
from .movedor import organizar


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

    carpeta = Path(args.carpeta)
    if not carpeta.is_dir():
        print(f"Error: '{carpeta}' no existe o no es una carpeta.", file=sys.stderr)
        sys.exit(1)

    try:
        reglas = cargar_reglas(args.reglas)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    movimientos = organizar(carpeta, reglas, simular=args.simular)

    if not movimientos:
        print("No había archivos para organizar.")
        return
    
    if args.simular:
        print("SIMULACIÓN: no se movió ningún archivo.")
        for origen, destino in movimientos:
            print(f"{origen.name} -> {destino.relative_to(carpeta)}")

    por_categoria = Counter(destino.parent.name for _, destino in movimientos)
    for categoria, cantidad in por_categoria.items():
        print(f"{categoria}: {cantidad}")
    print(f"Total: {len(movimientos)}")


if __name__ == "__main__":
    main()