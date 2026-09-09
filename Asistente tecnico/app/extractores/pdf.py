"""Extracción de texto y metadatos desde documentos PDF."""

from __future__ import annotations

from pathlib import Path


def extraer_pdf(ruta: Path) -> tuple[str, dict[str, str]]:
    """Devuelve el texto por página y metadatos básicos de un PDF."""
    try:
        from pypdf import PdfReader
    except ImportError as error:
        raise RuntimeError("Falta instalar 'pypdf' para extraer PDF.") from error

    lector = PdfReader(str(ruta))
    paginas = []
    for numero, pagina in enumerate(lector.pages, start=1):
        texto = pagina.extract_text() or ""
        paginas.append(f"[Página {numero}]\n{texto.strip()}".strip())
    contenido = "\n\n".join(paginas)
    if not contenido.strip():
        contenido = "[PDF sin texto extraíble; puede requerir OCR visual.]"
    metadata = lector.metadata or {}
    return contenido, {
        "tipo": "pdf",
        "paginas": str(len(lector.pages)),
        "titulo": str(metadata.get("/Title", "") or ""),
        "autor": str(metadata.get("/Author", "") or ""),
    }
