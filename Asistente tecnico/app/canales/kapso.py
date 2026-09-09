"""Adaptador mínimo y seguro para mensajes entrantes de Kapso.

No contiene credenciales ni decide acciones sobre una máquina. Convierte un
webhook de Kapso en una consulta al núcleo documental y envía su respuesta.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.servicios.asistente_tecnico import AsistenteTecnico
from app.servicios.registrar_error import registrar_consulta


EVENTO_MENSAJE_RECIBIDO = "whatsapp.message.received"


def firma_valida(cuerpo: bytes, firma: str | None, secreto: str) -> bool:
    """Comprueba la firma HMAC SHA-256 enviada por Kapso."""
    if not firma or not secreto:
        return False
    esperada = hmac.new(secreto.encode("utf-8"), cuerpo, hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperada, firma)


def extraer_mensajes(payload: dict) -> list[dict]:
    """Normaliza los formatos individual y agrupado de Kapso."""
    if payload.get("type") != EVENTO_MENSAJE_RECIBIDO:
        return []
    datos = payload.get("data")
    if isinstance(datos, list):
        return [item for item in datos if isinstance(item, dict) and isinstance(item.get("message"), dict)]
    if isinstance(datos, dict) and isinstance(datos.get("message"), dict):
        return [datos]
    return []


def texto_del_mensaje(mensaje: dict) -> str | None:
    if mensaje.get("type") != "text":
        return None
    texto = mensaje.get("text")
    if not isinstance(texto, dict):
        return None
    cuerpo = texto.get("body")
    return cuerpo.strip() if isinstance(cuerpo, str) and cuerpo.strip() else None


@dataclass
class SesionesKapso:
    """Estado efímero de la máquina elegida por cada empleado."""

    maquina_por_remitente: dict[str, str] = field(default_factory=dict)

    def seleccionar(self, remitente: str, texto: str) -> str | None:
        texto_normalizado = texto.strip().lower()
        opciones = {
            "1": "KDT-KD610HZ",
            "kdt": "KDT-KD610HZ",
            "flex": "KDT-KD610HZ",
            "ultraflex": "KDT-KD610HZ",
            "kdt-kd610hz": "KDT-KD610HZ",
        }
        maquina = opciones.get(texto_normalizado)
        if maquina:
            self.maquina_por_remitente[remitente] = maquina
        return maquina

    def maquina(self, remitente: str) -> str | None:
        return self.maquina_por_remitente.get(remitente)


class ClienteKapso:
    """Cliente HTTP pequeño para enviar texto mediante la API oficial de Kapso."""

    def __init__(self, api_key: str, phone_number_id: str) -> None:
        self.api_key = api_key
        self.phone_number_id = phone_number_id

    def enviar_texto(self, destinatario: str, texto: str) -> None:
        cuerpo = json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": destinatario,
                "type": "text",
                "text": {"body": texto[:4096]},
            },
            ensure_ascii=False,
        ).encode("utf-8")
        url = f"https://api.kapso.ai/meta/whatsapp/v24.0/{self.phone_number_id}/messages"
        solicitud = Request(
            url,
            data=cuerpo,
            headers={"Content-Type": "application/json", "X-API-Key": self.api_key},
            method="POST",
        )
        try:
            with urlopen(solicitud, timeout=10) as respuesta:
                if not 200 <= respuesta.status < 300:
                    raise RuntimeError(f"Kapso devolvió HTTP {respuesta.status}.")
        except (HTTPError, URLError) as error:
            raise RuntimeError("No se pudo enviar la respuesta por Kapso.") from error


class PuenteKapso:
    """Coordina el mensaje entrante con el asistente documental local."""

    TEXTO_BIENVENIDA = (
        "Asistente técnico de fábrica.\n\n"
        "Elegí la máquina escribiendo:\n"
        "1. Flex / KDT KD-610HZ\n\n"
        "Después enviá el código exacto de alarma o describí la falla. "
        "No se envían comandos ni indicaciones para intervenir con tensión."
    )

    def __init__(
        self,
        asistente: AsistenteTecnico,
        cliente: ClienteKapso,
        directorio_logs: Path,
        remitentes_autorizados: set[str] | None = None,
    ) -> None:
        self.asistente = asistente
        self.cliente = cliente
        self.directorio_logs = directorio_logs
        # Una lista vacía o nula habilita el número para toda persona que escriba.
        self.remitentes_autorizados = remitentes_autorizados or set()
        self.sesiones = SesionesKapso()
        self.consultas_recientes: dict[str, deque[datetime]] = defaultdict(deque)

    def procesar(self, entrada: dict) -> None:
        mensaje = entrada["message"]
        remitente = str(mensaje.get("from", ""))
        if not remitente or (self.remitentes_autorizados and remitente not in self.remitentes_autorizados):
            return
        if not self._dentro_del_limite(remitente):
            self.cliente.enviar_texto(
                remitente,
                "Recibimos varias consultas muy seguidas. Esperá unos minutos y volvemos a atenderte.",
            )
            return
        texto = texto_del_mensaje(mensaje)
        if texto is None:
            self.cliente.enviar_texto(
                remitente,
                "Recibí el archivo o foto. Para esta primera prueba, escribí también el código de alarma "
                "o una breve descripción de la falla.",
            )
            return
        if texto.lower() in {"hola", "menu", "menú", "ayuda", "inicio"}:
            self.cliente.enviar_texto(remitente, self.TEXTO_BIENVENIDA)
            return
        if self.sesiones.seleccionar(remitente, texto):
            self.cliente.enviar_texto(remitente, "Máquina seleccionada: Flex / KDT KD-610HZ. ¿Qué alarma o falla aparece?")
            return
        maquina = self.sesiones.maquina(remitente)
        if not maquina:
            self.cliente.enviar_texto(remitente, self.TEXTO_BIENVENIDA)
            return
        respuesta = self.asistente.responder(maquina, texto)
        self.cliente.enviar_texto(remitente, respuesta.texto)
        registrar_consulta(self.directorio_logs, maquina, texto, respuesta.texto)

    def _dentro_del_limite(self, remitente: str) -> bool:
        """Evita abuso sin almacenar números ni estados en un servicio externo."""
        ahora = datetime.now(timezone.utc)
        inicio_ventana = ahora - timedelta(minutes=15)
        recientes = self.consultas_recientes[remitente]
        while recientes and recientes[0] < inicio_ventana:
            recientes.popleft()
        if len(recientes) >= 12:
            return False
        recientes.append(ahora)
        return True


def configuracion_kapso_desde_entorno() -> tuple[str, str, str, set[str]]:
    """Lee configuración sin permitir valores secretos en el repositorio."""
    api_key = os.environ.get("KAPSO_API_KEY", "")
    phone_number_id = os.environ.get("KAPSO_PHONE_NUMBER_ID", "")
    secreto_webhook = os.environ.get("KAPSO_WEBHOOK_SECRET", "")
    autorizados = {numero.strip().lstrip("+") for numero in os.environ.get("KAPSO_ALLOWED_SENDERS", "").split(",") if numero.strip()}
    faltantes = [
        nombre
        for nombre, valor in {
            "KAPSO_API_KEY": api_key,
            "KAPSO_PHONE_NUMBER_ID": phone_number_id,
            "KAPSO_WEBHOOK_SECRET": secreto_webhook,
        }.items()
        if not valor
    ]
    if faltantes:
        raise RuntimeError("Faltan variables de entorno: " + ", ".join(faltantes))
    return api_key, phone_number_id, secreto_webhook, autorizados
