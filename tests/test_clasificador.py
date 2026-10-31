import pytest

from organizador.clasificador import obtener_categoria

REGLAS = {
    "Imágenes": (".jpg", ".png"),
    "Videos": (".mp4", ".mkv"),
}


@pytest.mark.parametrize(
    "nombre, esperado",
    [
        ("foto.jpg", "Imágenes"),
        ("FOTO.PNG", "Imágenes"),
        ("clip.MKV", "Videos"),
        ("sin_extension", "Otros"),
        ("archivo.desconocido", "Otros"),
        (".gitignore", "Otros"),
        ("copia.tar.gz", "Otros"),
    ],
)
def test_obtener_categoria(nombre, esperado):
    assert obtener_categoria(nombre, REGLAS) == esperado


def test_sin_reglas_todo_es_otros():
    assert obtener_categoria("foto.jpg", {}) == "Otros"