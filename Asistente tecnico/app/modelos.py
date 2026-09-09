"""Modelos simples usados entre los módulos del asistente."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Documento:
    maquina_id: str
    ruta: Path
    contenido: str


@dataclass(frozen=True)
class ResultadoBusqueda:
    documento: Documento
    puntuacion: int
    fragmento: str


@dataclass(frozen=True)
class RespuestaTecnica:
    texto: str
    resultados: tuple[ResultadoBusqueda, ...]


@dataclass(frozen=True)
class EntradaConversacion:
    sesion_id: str
    maquina_id: str
    consulta: str
    respuesta: str
    imagen: str | None = None
