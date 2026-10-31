import shutil
from pathlib import Path

import pytest

from organizador.movedor import organizar

REGLAS = {
    "Imágenes": (".jpg", ".png"),
    "Documentos": (".pdf", ".txt"),
}


def crear_archivos(carpeta, *nombres):
    """Crea archivos vacíos con los nombres dados dentro de la carpeta."""
    for nombre in nombres:
        (carpeta / nombre).touch()


def test_mueve_cada_archivo_a_su_categoria(tmp_path):
    crear_archivos(tmp_path, "foto.jpg", "informe.pdf", "raro.xyz")

    movimientos, errores = organizar(tmp_path, REGLAS)

    assert (tmp_path / "Imágenes" / "foto.jpg").exists()
    assert (tmp_path / "Documentos" / "informe.pdf").exists()
    assert (tmp_path / "Otros" / "raro.xyz").exists()
    assert len(movimientos) == 3
    assert errores == []


def test_no_deja_archivos_sueltos_en_la_raiz(tmp_path):
    crear_archivos(tmp_path, "foto.jpg", "informe.pdf", "sin_extension")

    organizar(tmp_path, REGLAS)

    assert [ruta for ruta in tmp_path.iterdir() if ruta.is_file()] == []


def test_no_toca_las_subcarpetas(tmp_path):
    subcarpeta = tmp_path / "proyecto"
    subcarpeta.mkdir()
    (subcarpeta / "notas.txt").touch()

    organizar(tmp_path, REGLAS)

    assert (subcarpeta / "notas.txt").exists()


def test_conflicto_de_nombre_no_sobrescribe(tmp_path):
    destino = tmp_path / "Imágenes"
    destino.mkdir()
    (destino / "foto.jpg").write_text("original")
    (tmp_path / "foto.jpg").write_text("nuevo")

    organizar(tmp_path, REGLAS)

    assert (destino / "foto.jpg").read_text() == "original"
    assert (destino / "foto (1).jpg").read_text() == "nuevo"


def test_conflictos_multiples_incrementan_el_contador(tmp_path):
    destino = tmp_path / "Documentos"
    destino.mkdir()
    (destino / "notas.txt").touch()
    (destino / "notas (1).txt").touch()
    (tmp_path / "notas.txt").touch()

    organizar(tmp_path, REGLAS)

    assert (destino / "notas (2).txt").exists()


def test_simular_no_modifica_el_disco(tmp_path):
    crear_archivos(tmp_path, "foto.jpg", "informe.pdf")

    movimientos, errores = organizar(tmp_path, REGLAS, simular=True)

    assert len(movimientos) == 2
    assert (tmp_path / "foto.jpg").exists()
    assert not (tmp_path / "Imágenes").exists()


def test_simular_predice_lo_que_hace_la_ejecucion_real(tmp_path):
    destino = tmp_path / "Imágenes"
    destino.mkdir()
    (destino / "foto.jpg").touch()
    (tmp_path / "foto.jpg").touch()

    simulados, _ = organizar(tmp_path, REGLAS, simular=True)
    reales, _ = organizar(tmp_path, REGLAS)

    assert simulados == reales


@pytest.mark.parametrize(
    "nombre",
    ["video.crdownload", "bajando.part", "TEMP.TMP", "desktop.ini", "Thumbs.db"],
)
def test_ignora_temporales_y_archivos_del_sistema(tmp_path, nombre):
    crear_archivos(tmp_path, nombre)

    movimientos, errores = organizar(tmp_path, REGLAS)

    assert movimientos == []
    assert (tmp_path / nombre).exists()


def test_segunda_ejecucion_no_hace_nada(tmp_path):
    crear_archivos(tmp_path, "foto.jpg", "informe.pdf")
    organizar(tmp_path, REGLAS)

    movimientos, errores = organizar(tmp_path, REGLAS)

    assert movimientos == []


def test_un_error_no_detiene_a_los_demas(tmp_path, monkeypatch):
    crear_archivos(tmp_path, "bloqueado.jpg", "libre.pdf")
    mover_original = shutil.move

    def mover_con_fallo(origen, destino):
        if Path(origen).name == "bloqueado.jpg":
            raise PermissionError(13, "Archivo en uso")
        return mover_original(origen, destino)

    monkeypatch.setattr("organizador.movedor.shutil.move", mover_con_fallo)

    movimientos, errores = organizar(tmp_path, REGLAS)

    assert len(movimientos) == 1
    assert len(errores) == 1
    assert errores[0][0].name == "bloqueado.jpg"
    assert (tmp_path / "bloqueado.jpg").exists()
    assert (tmp_path / "Documentos" / "libre.pdf").exists()