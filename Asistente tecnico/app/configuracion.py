"""Configuración central del proyecto, sin lógica de negocio."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Configuracion:
    raiz_proyecto: Path
    archivo_maquinas: Path
    archivo_guias_diagnostico: Path
    directorio_indice: Path
    directorio_logs: Path


def cargar_configuracion(raiz_proyecto: Path) -> Configuracion:
    raiz_proyecto = raiz_proyecto.resolve()
    return Configuracion(
        raiz_proyecto=raiz_proyecto,
        archivo_maquinas=raiz_proyecto / "datos" / "maquinas.json",
        archivo_guias_diagnostico=raiz_proyecto / "datos" / "guias_diagnostico.json",
        directorio_indice=raiz_proyecto / "datos" / "indice_documentacion",
        directorio_logs=raiz_proyecto / "logs",
    )


def cargar_maquinas(config: Configuracion) -> dict[str, dict[str, str]]:
    with config.archivo_maquinas.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos["maquinas"]
