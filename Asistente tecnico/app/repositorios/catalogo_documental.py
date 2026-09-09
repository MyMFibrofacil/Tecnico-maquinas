"""Carga y búsqueda básica sobre la documentación de cada máquina."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from app.configuracion import Configuracion, cargar_maquinas
from app.extractores.orquestador import extraer_archivo, extensiones_soportadas
from app.modelos import Documento, ResultadoBusqueda


class CatalogoDocumental:
    EXTENSIONES_TEXTO = {".md", ".txt", ".jsonl"}

    def __init__(self, config: Configuracion) -> None:
        self.config = config
        self.maquinas = cargar_maquinas(config)

    def reconstruir_indice(self) -> int:
        self.config.directorio_indice.mkdir(parents=True, exist_ok=True)
        documentos = list(self._cargar_documentos())
        manifiesto = self.config.directorio_indice / "manifest.jsonl"
        contenido_indexado = self.config.directorio_indice / "documentos.jsonl"
        registros = []
        documentos_compactos = []
        for documento in documentos:
            clave = hashlib.sha1(str(documento.ruta).encode("utf-8")).hexdigest()[:16]
            destino = self.config.directorio_indice / f"{documento.maquina_id}__{clave}.txt"
            destino.write_text(documento.contenido, encoding="utf-8")
            registros.append({"maquina_id": documento.maquina_id, "origen": str(documento.ruta), "indice": destino.name})
            documentos_compactos.append({"maquina_id": documento.maquina_id, "origen": str(documento.ruta), "contenido": documento.contenido})
        manifiesto.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in registros) + "\n", encoding="utf-8")
        contenido_indexado.write_text(
            "\n".join(json.dumps(item, ensure_ascii=False) for item in documentos_compactos) + "\n",
            encoding="utf-8",
        )
        return len(documentos)

    def buscar(self, maquina_id: str, consulta: str, limite: int = 5) -> list[ResultadoBusqueda]:
        documentos = [d for d in self._cargar_documentos_consulta() if d.maquina_id == maquina_id]
        tokens = self._tokens(consulta)
        resultados: list[ResultadoBusqueda] = []
        for documento in documentos:
            tokens_contenido = self._tokens(documento.contenido)
            puntuacion = sum(token in tokens_contenido for token in tokens)
            if any(token in documento.contenido.lower() for token in tokens):
                puntuacion += 2
            if documento.ruta.name.lower().startswith("informe_"):
                puntuacion += 1
            if puntuacion:
                resultados.append(ResultadoBusqueda(documento, puntuacion, self._fragmento(documento.contenido, tokens)))
        return sorted(resultados, key=lambda item: item.puntuacion, reverse=True)[:limite]

    def _cargar_documentos_consulta(self):
        """Usa el índice extraído cuando existe; si no, lee las fuentes directamente."""
        contenido_indexado = self.config.directorio_indice / "documentos.jsonl"
        if contenido_indexado.exists():
            try:
                for linea in contenido_indexado.read_text(encoding="utf-8").splitlines():
                    registro = json.loads(linea)
                    yield Documento(registro["maquina_id"], Path(registro["origen"]), registro["contenido"])
                return
            except (OSError, json.JSONDecodeError, KeyError):
                pass
        manifiesto = self.config.directorio_indice / "manifest.jsonl"
        if not manifiesto.exists():
            yield from self._cargar_documentos()
            return
        try:
            for linea in manifiesto.read_text(encoding="utf-8").splitlines():
                registro = json.loads(linea)
                indice = self.config.directorio_indice / registro["indice"]
                if indice.exists():
                    yield Documento(
                        registro["maquina_id"],
                        Path(registro["origen"]),
                        indice.read_text(encoding="utf-8", errors="replace"),
                    )
        except (OSError, json.JSONDecodeError, KeyError):
            yield from self._cargar_documentos()

    def _cargar_documentos(self):
        for maquina_id, datos in self.maquinas.items():
            raiz = Path(datos["directorio_documentacion"])
            if not raiz.is_absolute():
                raiz = (self.config.raiz_proyecto / raiz).resolve()
            if not raiz.exists():
                continue
            for ruta in raiz.rglob("*"):
                extension = ruta.suffix.lower()
                if ruta.is_file() and extension in self.EXTENSIONES_TEXTO and ruta.stem.lower() not in {"readme", "test"}:
                    try:
                        yield Documento(maquina_id, ruta, ruta.read_text(encoding="utf-8", errors="replace"))
                    except OSError:
                        continue
                elif ruta.is_file() and extension in extensiones_soportadas():
                    try:
                        contenido, _ = extraer_archivo(ruta)
                        yield Documento(maquina_id, ruta, contenido)
                    except (OSError, RuntimeError):
                        continue

    @staticmethod
    def _tokens(texto: str) -> set[str]:
        return {token for token in re.findall(r"[a-záéíóúüñ0-9-]{3,}", texto.lower())}

    @staticmethod
    def _fragmento(contenido: str, tokens: set[str], limite: int = 500) -> str:
        lineas = contenido.splitlines()
        for indice, linea in enumerate(lineas):
            if any(token in linea.lower() for token in tokens):
                inicio = max(0, indice - 1)
                return " ".join(lineas[inicio : indice + 3])[:limite]
        return contenido[:limite].replace("\n", " ")
