"""Registro append-only de casos recibidos por el asistente."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def registrar_consulta(directorio_logs: Path, maquina_id: str, consulta: str, resultado: str) -> Path:
    directorio_logs.mkdir(parents=True, exist_ok=True)
    ruta = directorio_logs / "consultas.jsonl"
    evento = {
        "fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
        "maquina_id": maquina_id,
        "consulta": consulta,
        "resultado": resultado,
    }
    with ruta.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")
    return ruta
