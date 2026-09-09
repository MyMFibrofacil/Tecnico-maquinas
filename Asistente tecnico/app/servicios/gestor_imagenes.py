"""Validación local de imágenes recibidas durante una conversación."""

from __future__ import annotations

from pathlib import Path


EXTENSIONES_IMAGEN = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def validar_ruta_imagen(ruta_texto: str) -> tuple[bool, str]:
    """Comprueba que una ruta local exista y tenga una extensión de imagen."""
    ruta = Path(ruta_texto.strip()).expanduser()
    if not ruta.exists():
        return False, "No encontré esa foto en la ruta indicada."
    if not ruta.is_file():
        return False, "La ruta indicada no corresponde a un archivo."
    if ruta.suffix.lower() not in EXTENSIONES_IMAGEN:
        return False, "El archivo no parece ser una imagen compatible."
    return True, str(ruta.resolve())
