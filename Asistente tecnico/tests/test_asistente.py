"""Pruebas mínimas del núcleo sin conexión a máquina ni WhatsApp."""

from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from app.configuracion import cargar_configuracion
from app.repositorios.catalogo_documental import CatalogoDocumental
from app.servicios.asistente_tecnico import AsistenteTecnico
from app.servicios.gestor_imagenes import validar_ruta_imagen


class AsistenteTecnicoTests(unittest.TestCase):
    def test_valida_imagen_existente(self):
        with TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "alarma.jpg"
            ruta.write_bytes(b"imagen de prueba")
            valido, resultado = validar_ruta_imagen(str(ruta))
            self.assertTrue(valido)
            self.assertEqual(resultado, str(ruta.resolve()))

    def test_rechaza_imagen_inexistente(self):
        valido, resultado = validar_ruta_imagen("C:/ruta/inexistente/alarma.jpg")
        self.assertFalse(valido)
        self.assertIn("No encontré", resultado)

    def test_consulta_sin_maquina_conocida(self):
        with TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            (raiz / "datos").mkdir()
            (raiz / "datos" / "maquinas.json").write_text(json.dumps({"maquinas": {}}), encoding="utf-8")
            config = cargar_configuracion(raiz)
            asistente = AsistenteTecnico(config, CatalogoDocumental(config))
            respuesta = asistente.responder("DESCONOCIDA", "alarma")
            self.assertIn("No conozco", respuesta.texto)

    def test_busca_en_documentacion_configurada(self):
        with TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            docs = raiz / "docs"
            docs.mkdir()
            (docs / "manual.md").write_text("Código Er2-6 del eje A", encoding="utf-8")
            (raiz / "datos").mkdir()
            (raiz / "datos" / "maquinas.json").write_text(
                json.dumps({"maquinas": {"KDT": {"directorio_documentacion": str(docs)}}}), encoding="utf-8"
            )
            config = cargar_configuracion(raiz)
            asistente = AsistenteTecnico(config, CatalogoDocumental(config))
            respuesta = asistente.responder("KDT", "Er2-6 eje A")
            self.assertTrue(respuesta.resultados)
            self.assertIn("Er2-6", respuesta.texto)


if __name__ == "__main__":
    unittest.main()
