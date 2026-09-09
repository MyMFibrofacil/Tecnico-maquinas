"""Lectura segura de estructura y muestras de bases SQLite."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


def _identificador(nombre: str) -> str:
    return '"' + nombre.replace('"', '""') + '"'


def extraer_sqlite(ruta: Path, limite_filas: int = 100) -> tuple[str, dict[str, str]]:
    """Lee SQLite en modo solo lectura, con esquema y hasta ``limite_filas`` por tabla."""
    uri = f"file:{ruta.as_posix()}?mode=ro"
    try:
        conexion = sqlite3.connect(uri, uri=True)
    except sqlite3.Error as error:
        raise RuntimeError(f"No se pudo abrir SQLite en modo solo lectura: {error}") from error

    bloques: list[str] = []
    try:
        conexion.execute("PRAGMA query_only = ON")
        tablas = conexion.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        for (tabla,) in tablas:
            columnas = conexion.execute(f"PRAGMA table_info({_identificador(tabla)})").fetchall()
            nombres = [fila[1] for fila in columnas]
            filas = conexion.execute(f"SELECT * FROM {_identificador(tabla)} LIMIT ?", (limite_filas,)).fetchall()
            bloque = [f"[Tabla: {tabla}]", "Columnas: " + ", ".join(nombres)]
            for fila in filas:
                bloque.append(json.dumps(dict(zip(nombres, fila)), ensure_ascii=False, default=str))
            bloques.append("\n".join(bloque))
    except sqlite3.Error as error:
        raise RuntimeError(f"Error leyendo SQLite: {error}") from error
    finally:
        conexion.close()

    return "\n\n".join(bloques) or "[SQLite sin tablas de usuario.]", {
        "tipo": "sqlite",
        "tablas": str(len(tablas)),
        "limite_filas": str(limite_filas),
    }
