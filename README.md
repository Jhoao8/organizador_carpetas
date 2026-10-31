# Organizador de Carpetas

Herramienta de línea de comandos en Python que ordena los archivos de cualquier carpeta en subcarpetas por categoría (Imágenes, Documentos, Videos, etc.), sin perder ni sobrescribir nada.

## Características

- Clasifica por extensión, sin distinguir mayúsculas de minúsculas.
- Reglas personalizables mediante un archivo JSON.
- Modo simulación (`--simular`): muestra qué haría sin mover nada.
- Nunca sobrescribe: si el nombre ya existe, renombra a `archivo (1).ext`.
- Ignora descargas en curso (`.crdownload`, `.part`, `.tmp`) y archivos del sistema (`desktop.ini`, `Thumbs.db`).
- Un archivo bloqueado no detiene la ejecución: se informa y se continúa.
- Registro de cada movimiento en un archivo de log.
- Lanzadores para Windows: úsalo desde cualquier carpeta, por terminal o arrastrando.
- Sin dependencias externas para ejecutarlo.

## Requisitos

- Python 3.10 o superior.
- Probado en Windows.

## Instalación

```powershell
git clone https://github.com/Jhoao8/organizador_carpetas.git
cd organizador_carpetas
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` solo incluye `pytest`, necesario únicamente para correr las pruebas.

## Uso

Recomendación: ejecuta siempre primero con `--simular`.

### Con Python

Desde la raíz del repositorio, con el entorno virtual activo:

```powershell
python -m organizador.cli RUTA [--reglas ARCHIVO.json] [--simular]
```

| Argumento | Descripción |
|---|---|
| `RUTA` | Carpeta a organizar (obligatorio). Acepta `.` para la carpeta actual. |
| `--reglas` | Archivo JSON con reglas propias. Si se omite, se usan las reglas por defecto. |
| `--simular` | Muestra los movimientos sin ejecutarlos. |

### Lanzadores para Windows

Permiten organizar **cualquier carpeta** sin activar el entorno virtual. Usan el `.venv` de la raíz del repo, por lo que deben permanecer junto a él.

| Lanzador | Uso |
|---|---|
| `organizar.bat` | Desde cualquier ubicación: `organizar.bat RUTA [--simular]`. |
| `organizar_arrastrando.bat` | Arrastra una carpeta sobre el archivo: simula, muestra el resultado y pide confirmación. |

Opciones adicionales:

- **Comando `organizar`:** agrega la raíz del repo al `Path` de Windows y ejecuta `organizar . --simular` en cualquier carpeta.
- **Clic derecho:** crea un acceso directo a `organizar_arrastrando.bat` en `shell:sendto` y úsalo desde **Enviar a**.

### Ejemplo

```
> organizar.bat C:\Users\yo\Downloads --simular
SIMULACIÓN: no se movió ningún archivo.
foto1.jpg -> Imágenes\foto1.jpg
informe.pdf -> Documentos\informe.pdf
Imágenes: 1
Documentos: 1
Total: 2
Registro: C:\Users\yo\.organizador\organizador.log
```

Sin `--simular`, los archivos se mueven y se muestra solo el resumen por categoría.

## Reglas personalizadas

Un archivo JSON que asocia cada categoría con una lista de extensiones:

```json
{
    "Fotos": [".jpg", ".png"],
    "Libros": [".epub", ".pdf"]
}
```

- Las extensiones empiezan con punto; se normalizan a minúsculas.
- Lo que no coincida con ninguna categoría va a `Otros`.
- Las reglas propias **reemplazan** a las de por defecto.
- Las reglas por defecto están en [`organizador/reglas_por_defecto.json`](organizador/reglas_por_defecto.json).

## Registro (log)

Cada ejecución agrega líneas a `~/.organizador/organizador.log` (en Windows, `C:\Users\<usuario>\.organizador\organizador.log`). Se registra el inicio, cada archivo movido o simulado, los errores y el fin.

## Pruebas

```powershell
pytest
```

## Estructura

```
organizador_carpetas/
├── organizador/
│   ├── clasificador.py        # decide la categoría de un archivo
│   ├── configuracion.py       # carga y valida las reglas JSON
│   ├── movedor.py             # mueve archivos, resuelve conflictos, ignora temporales
│   ├── registro.py            # configuración del log
│   ├── cli.py                 # interfaz de línea de comandos
│   └── reglas_por_defecto.json
├── tests/                     # pruebas con pytest
├── organizar.bat              # lanzador para usar en cualquier carpeta
├── organizar_arrastrando.bat  # lanzador de arrastrar y soltar
├── pytest.ini
├── requirements.txt
└── LICENSE
```

## Limitaciones conocidas

- Con extensiones dobles (`.tar.gz`) solo se considera la última (`.gz`).
- Solo procesa los archivos de la carpeta indicada, no sus subcarpetas.
- No tiene función de deshacer.

## Licencia

MIT