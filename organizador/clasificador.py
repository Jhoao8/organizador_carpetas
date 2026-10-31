from pathlib import Path

CATEGORIAS = {
    "Imágenes": (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg",),
    "Documentos": (".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv",),
    "Videos": (".mp4", ".mkv", ".avi", ".mov",),
    "Comprimidos": (".zip", ".rar", ".7z", ".tar", ".gz",),
    "Instaladores": (".exe", ".msi",)
}


def obtener_categoria(nombre_archivo):
    """Recibe un nombre de archivo y devuelve el nombre de su categoría"""
    extension = Path(nombre_archivo).suffix.lower()
    for categoria, extensiones in CATEGORIAS.items():
        if extension in extensiones:
            return categoria
    return "Otros"