"""Pruebas del adaptador Kapso sin conexión a la API externa."""

import hashlib
import hmac
import json
import unittest
from pathlib import Path
from unittest.mock import Mock

from app.canales.kapso import EVENTO_MENSAJE_RECIBIDO, PuenteKapso, extraer_mensajes, firma_valida, texto_del_mensaje


class KapsoTests(unittest.TestCase):
    def test_valida_firma(self):
        cuerpo = b'{"type":"prueba"}'
        secreto = "secreto-de-prueba"
        firma = hmac.new(secreto.encode(), cuerpo, hashlib.sha256).hexdigest()
        self.assertTrue(firma_valida(cuerpo, firma, secreto))
        self.assertFalse(firma_valida(cuerpo, "invalida", secreto))

    def test_extrae_mensaje_individual(self):
        payload = {
            "type": EVENTO_MENSAJE_RECIBIDO,
            "data": {"message": {"from": "5491100000000", "type": "text", "text": {"body": " Er2-6 "}}},
        }
        mensajes = extraer_mensajes(payload)
        self.assertEqual(len(mensajes), 1)
        self.assertEqual(texto_del_mensaje(mensajes[0]["message"]), "Er2-6")

    def test_ignora_evento_distinto(self):
        self.assertEqual(extraer_mensajes({"type": "whatsapp.message.read", "data": {}}), [])

    def test_admite_remitente_cualquiera_si_no_hay_lista(self):
        cliente = Mock()
        puente = PuenteKapso(Mock(), cliente, Path("."))
        puente.procesar({"message": {"from": "5491100000000", "type": "text", "text": {"body": "hola"}}})
        cliente.enviar_texto.assert_called_once()


if __name__ == "__main__":
    unittest.main()
