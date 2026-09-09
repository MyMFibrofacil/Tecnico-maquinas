"""Proveedor opcional para interpretar fotos y redactar respuestas técnicas.

No se realiza ninguna llamada si OPENAI_API_KEY no está configurada.
"""

from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path


class ProveedorOpenAI:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.modelo = os.getenv("OPENAI_MODEL", "gpt-5")

    @property
    def disponible(self) -> bool:
        return bool(self.api_key)

    def analizar_foto(self, foto: Path, consulta: str, respuesta_documental: str) -> str:
        if not self.disponible:
            raise RuntimeError("OPENAI_API_KEY no está configurada.")

        try:
            from openai import OpenAI
        except ImportError as error:
            raise RuntimeError("Falta instalar el paquete opcional 'openai'.") from error

        tipo_mime = mimetypes.guess_type(foto.name)[0] or "image/jpeg"
        imagen = base64.b64encode(foto.read_bytes()).decode("ascii")
        cliente = OpenAI(api_key=self.api_key)
        response = cliente.responses.create(
            model=self.modelo,
            instructions=(
                "Sos un asistente técnico de mantenimiento. Respondé en español, de forma breve. "
                "No controles máquinas, no indiques puentear seguridades ni modificar parámetros. "
                "Diferenciá hechos observados de hipótesis y pedí una foto o dato adicional si falta información."
            ),
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"Consulta: {consulta}\n\nAnálisis documental local:\n{respuesta_documental}"},
                    {"type": "input_image", "image_url": f"data:{tipo_mime};base64,{imagen}"},
                ],
            }],
        )
        return response.output_text.strip()
