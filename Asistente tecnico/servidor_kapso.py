"""Servidor local de desarrollo para recibir webhooks de Kapso.

Uso: python servidor_kapso.py
Requiere un túnel HTTPS o un servidor público para que Kapso pueda alcanzarlo.
"""

from __future__ import annotations

import argparse
import json
import logging
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from app.canales.kapso import (
    PuenteKapso,
    ClienteKapso,
    configuracion_kapso_desde_entorno,
    extraer_mensajes,
    firma_valida,
)
from app.configuracion import cargar_configuracion
from app.repositorios.catalogo_documental import CatalogoDocumental
from app.servicios.asistente_tecnico import AsistenteTecnico


def construir_servidor(host: str, puerto: int) -> ThreadingHTTPServer:
    config = cargar_configuracion(Path(__file__).parent)
    api_key, phone_number_id, secreto, autorizados = configuracion_kapso_desde_entorno()
    puente = PuenteKapso(
        AsistenteTecnico(config, CatalogoDocumental(config)),
        ClienteKapso(api_key, phone_number_id),
        config.directorio_logs,
        autorizados,
    )
    idempotencias: deque[str] = deque(maxlen=1000)

    class ManejadorKapso(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/webhooks/kapso":
                self.send_error(404)
                return
            longitud = int(self.headers.get("Content-Length", "0"))
            if not 0 < longitud <= 1_000_000:
                self.send_error(413)
                return
            cuerpo = self.rfile.read(longitud)
            if not firma_valida(cuerpo, self.headers.get("X-Webhook-Signature"), secreto):
                self.send_error(401)
                return
            clave = self.headers.get("X-Idempotency-Key")
            if clave and clave in idempotencias:
                self.send_response(200)
                self.end_headers()
                return
            try:
                payload = json.loads(cuerpo)
            except json.JSONDecodeError:
                self.send_error(400)
                return
            if clave:
                idempotencias.append(clave)
            self.send_response(200)
            self.end_headers()
            for entrada in extraer_mensajes(payload):
                try:
                    puente.procesar(entrada)
                except RuntimeError:
                    logging.exception("No se pudo procesar el mensaje de Kapso")

        def log_message(self, formato: str, *argumentos: object) -> None:
            logging.info("Kapso: " + formato, *argumentos)

    return ThreadingHTTPServer((host, puerto), ManejadorKapso)


def main() -> int:
    parser = argparse.ArgumentParser(description="Receptor local de webhooks Kapso")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--puerto", type=int, default=8787)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    servidor = construir_servidor(args.host, args.puerto)
    print(f"Escuchando Kapso en http://{args.host}:{args.puerto}/webhooks/kapso")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
