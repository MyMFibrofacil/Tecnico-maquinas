"""Modo de prueba conversacional local, sin conexión externa."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from app.configuracion import Configuracion
from app.servicios.asistente_tecnico import AsistenteTecnico
from app.servicios.gestor_imagenes import validar_ruta_imagen
from app.servicios.proveedor_openai import ProveedorOpenAI


class ConversacionLocal:
    def __init__(self, config: Configuracion, asistente: AsistenteTecnico, sesion_id: str | None = None) -> None:
        self.config = config
        self.asistente = asistente
        self.sesion_id = sesion_id or uuid4().hex[:12]
        self.maquina_id: str | None = None
        self.historial: list[dict[str, str]] = []
        self.proveedor_openai = ProveedorOpenAI()

    def ejecutar(self, maquina_id: str | None = None) -> None:
        self.maquina_id = maquina_id
        print(f"Sesión local: {self.sesion_id}")
        print("Comandos: /maquina CODIGO, /foto RUTA, /historial, /salir")
        while True:
            consulta = input("\nEmpleado: ").strip()
            if not consulta:
                continue
            if consulta.lower() == "/salir":
                print("Sesión finalizada.")
                return
            if consulta.lower() == "/historial":
                self._mostrar_historial()
                continue
            if consulta.lower().startswith("/maquina "):
                self.maquina_id = consulta.split(maxsplit=1)[1].strip()
                print(f"Máquina seleccionada: {self.maquina_id}")
                continue
            if not self.maquina_id:
                print("Primero indique la máquina con /maquina KDT-KD610HZ")
                continue
            imagen = None
            if consulta.lower().startswith("/foto "):
                valido, resultado = validar_ruta_imagen(consulta.split(maxsplit=1)[1])
                if not valido:
                    print(f"Foto: {resultado}")
                    continue
                imagen = resultado
                consulta = input("Descripción de la alarma: ").strip()
            respuesta = self.asistente.responder(self.maquina_id, consulta)
            if imagen:
                respuesta_texto = respuesta.texto + "\n\nRuta de la foto registrada para análisis visual posterior."
                if self.proveedor_openai.disponible:
                    try:
                        respuesta_texto = self.proveedor_openai.analizar_foto(Path(imagen), consulta, respuesta.texto)
                    except (OSError, RuntimeError) as error:
                        respuesta_texto += f"\n\nNo se pudo analizar visualmente la foto: {error}"
            else:
                respuesta_texto = respuesta.texto
            print(f"\nAsistente:\n{respuesta_texto}")
            self._guardar(consulta, respuesta_texto, imagen)
            self.historial.append({"consulta": consulta, "respuesta": respuesta_texto})

    def _mostrar_historial(self) -> None:
        if not self.historial:
            print("Todavía no hay consultas en esta sesión.")
            return
        for indice, entrada in enumerate(self.historial[-5:], start=1):
            print(f"{indice}. {entrada['consulta']}")

    def _guardar(self, consulta: str, respuesta: str, imagen: str | None) -> None:
        self.config.directorio_logs.mkdir(parents=True, exist_ok=True)
        ruta = self.config.directorio_logs / "conversaciones.jsonl"
        evento = {
            "fecha": datetime.now().astimezone().isoformat(timespec="seconds"),
            "sesion_id": self.sesion_id,
            "maquina_id": self.maquina_id,
            "consulta": consulta,
            "respuesta": respuesta,
            "imagen": imagen,
        }
        with ruta.open("a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")
