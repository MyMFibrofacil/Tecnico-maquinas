"""Extracción de metadatos y texto OCR desde fotografías."""

from __future__ import annotations

from pathlib import Path


def extraer_imagen(ruta: Path, realizar_ocr: bool = True) -> tuple[str, dict[str, str]]:
    """Devuelve metadatos de la imagen y OCR si Pillow/Tesseract están disponibles."""
    try:
        from PIL import Image
    except ImportError as error:
        raise RuntimeError("Falta instalar 'Pillow' para leer fotografías.") from error

    with Image.open(ruta) as imagen:
        ancho, alto = imagen.size
        modo = imagen.mode
        formato = imagen.format or ruta.suffix.lstrip(".").upper()
        texto_ocr = ""
        estado_ocr = "no solicitado"
        if realizar_ocr:
            try:
                import pytesseract

                texto_ocr = pytesseract.image_to_string(imagen).strip()
                estado_ocr = "texto encontrado" if texto_ocr else "sin texto detectado"
            except (ImportError, OSError, RuntimeError) as error:
                estado_ocr = f"no disponible: {error}"

    contenido = f"[Imagen: {ruta.name}]\nDimensiones: {ancho} x {alto}\nFormato: {formato}\nModo: {modo}\nOCR: {estado_ocr}"
    if texto_ocr:
        contenido += f"\n\n[Texto OCR]\n{texto_ocr}"
    return contenido, {
        "tipo": "imagen",
        "ancho": str(ancho),
        "alto": str(alto),
        "formato": str(formato),
        "ocr": estado_ocr,
    }
