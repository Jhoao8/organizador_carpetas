import argparse
import sys
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

    resumen = organizar(carpeta, reglas)

    if not resumen:
        print("No había archivos para organizar.")
    else:
        for categoria, cantidad in resumen.items():
            print(f"{categoria}: {cantidad}")
        print(f"Total: {sum(resumen.values())}")


if __name__ == "__main__":
    main()