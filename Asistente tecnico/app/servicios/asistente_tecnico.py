"""Genera respuestas técnicas seguras a partir de fuentes documentales."""

from __future__ import annotations

import json

from app.configuracion import Configuracion, cargar_maquinas
from app.modelos import RespuestaTecnica
from app.repositorios.catalogo_documental import CatalogoDocumental
from app.servicios.analizar_falla import buscar_caso_historico, extraer_codigo, formatear_guia_whatsapp, formatear_whatsapp


class AsistenteTecnico:
    def __init__(self, config: Configuracion, catalogo: CatalogoDocumental) -> None:
        self.config = config
        self.catalogo = catalogo
        self.maquinas = cargar_maquinas(config)
        if config.archivo_guias_diagnostico.exists():
            with config.archivo_guias_diagnostico.open("r", encoding="utf-8") as archivo:
                self.guias = json.load(archivo)
        else:
            self.guias = {}

    def responder(self, maquina_id: str, consulta: str) -> RespuestaTecnica:
        if maquina_id not in self.maquinas:
            return RespuestaTecnica(f"No conozco la máquina '{maquina_id}'. Primero debe incorporarse al catálogo.", ())

        documentos = [documento for documento in self.catalogo._cargar_documentos_consulta() if documento.maquina_id == maquina_id]
        resultados = tuple(self.catalogo.buscar(maquina_id, consulta))
        caso = buscar_caso_historico(documentos, consulta)
        if caso:
            codigo = extraer_codigo(consulta)
            guia = self.guias.get(codigo) if codigo else None
            texto = formatear_whatsapp(caso, guia)
            return RespuestaTecnica(texto, resultados)
        codigo = extraer_codigo(consulta)
        if codigo and codigo in self.guias:
            return RespuestaTecnica(formatear_guia_whatsapp(codigo, self.guias[codigo]), resultados)
        if not resultados:
            texto = (
                "No encontré una coincidencia suficiente en la documentación de esta máquina. "
                "Envíe el código exacto, el eje o componente involucrado y una foto de la pantalla."
            )
            return RespuestaTecnica(texto, ())

        fuentes = "\n".join(f"- {resultado.documento.ruta}" for resultado in resultados)
        fragmentos = "\n\n".join(f"[{resultado.documento.ruta.name}] {resultado.fragmento}" for resultado in resultados)
        texto = (
            "Análisis documental preliminar (no constituye una confirmación de la causa):\n\n"
            f"{fragmentos}\n\n"
            "Verificaciones sugeridas: confirmar el código completo, el eje o componente, "
            "el estado de seguridad y las condiciones visibles antes de intervenir físicamente.\n\n"
            f"Fuentes consultadas:\n{fuentes}"
        )
        return RespuestaTecnica(texto, resultados)
