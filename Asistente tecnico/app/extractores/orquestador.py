"""Selecciona el extractor adecuado según la extensión del archivo."""

from __future__ import annotations

from pathlib import Path

from app.extractores.excel import extraer_excel
from app.extractores.imagenes import extraer_imagen
from app.extractores.pdf import extraer_pdf
from app.extractores.sqlite import extraer_sqlite


def extensiones_soportadas() -> set[str]:
    return {".pdf", ".xlsx", ".xlsm", ".xltx", ".xltm", ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".db", ".sqlite", ".sqlite3"}


def extraer_archivo(ruta: Path) -> tuple[str, dict[str, str]]:
    """Extrae contenido del archivo; lanza un error claro si no hay extractor."""
    extension = ruta.suffix.lower()
    if extension == ".pdf":
        return extraer_pdf(ruta)
    if extension in {".xlsx", ".xlsm", ".xltx", ".xltm"}:
        return extraer_excel(ruta)
    if extension in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
        return extraer_imagen(ruta)
    if extension in {".db", ".sqlite", ".sqlite3"}:
        return extraer_sqlite(ruta)
    raise RuntimeError(f"No hay extractor para la extensión {extension}.")
