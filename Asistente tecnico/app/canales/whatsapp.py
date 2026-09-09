"""Contrato inicial para conectar WhatsApp en una etapa posterior.

Este módulo no realiza llamadas externas ni contiene credenciales.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MensajeWhatsApp:
    identificador_empleado: str
    maquina_id: str
    texto: str
    imagen: bytes | None = None


class AdaptadorWhatsApp:
    """Interfaz deliberadamente pequeña para no acoplar el núcleo al proveedor."""

    def recibir(self) -> MensajeWhatsApp:
        raise NotImplementedError("La conexión WhatsApp se implementará en la siguiente etapa.")

    def enviar(self, identificador_empleado: str, texto: str) -> None:
        raise NotImplementedError("La conexión WhatsApp se implementará en la siguiente etapa.")
