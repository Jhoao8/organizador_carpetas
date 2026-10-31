import pytest

from organizador.configuracion import cargar_reglas


def escribir_json(ruta, contenido):
    """Crea un archivo de texto UTF-8 con el contenido dado y devuelve su ruta."""
    ruta.write_text(contenido, encoding="utf-8")
    return ruta


def test_reglas_por_defecto_se_cargan():
    reglas = cargar_reglas()
    assert ".jpg" in reglas["Imágenes"]


def test_cargar_reglas_propias(tmp_path):
    ruta = escribir_json(tmp_path / "reglas.json", '{"Fotos": [".jpg", ".png"]}')
    assert cargar_reglas(ruta) == {"Fotos": (".jpg", ".png")}


def test_acepta_la_ruta_como_texto(tmp_path):
    ruta = escribir_json(tmp_path / "reglas.json", '{"Fotos": [".jpg"]}')
    assert cargar_reglas(str(ruta)) == {"Fotos": (".jpg",)}


def test_normaliza_extensiones_a_minusculas(tmp_path):
    ruta = escribir_json(tmp_path / "reglas.json", '{"Fotos": [".JPG", ".Png"]}')
    assert cargar_reglas(ruta) == {"Fotos": (".jpg", ".png")}


def test_archivo_inexistente(tmp_path):
    with pytest.raises(ValueError, match="No se encontró"):
        cargar_reglas(tmp_path / "no_existe.json")


@pytest.mark.parametrize(
    "contenido, mensaje",
    [
        ('{"Fotos": [".jpg",]}', "no es un JSON válido"),
        ('[".jpg"]', "debe contener un objeto"),
        ('{"Fotos": ".jpg"}', "debe tener una lista"),
        ('{"Fotos": ["jpg"]}', "empiecen con punto"),
        ('{"Fotos": [1, 2]}', "empiecen con punto"),
    ],
)
def test_reglas_invalidas(tmp_path, contenido, mensaje):
    ruta = escribir_json(tmp_path / "malo.json", contenido)
    with pytest.raises(ValueError, match=mensaje):
        cargar_reglas(ruta)