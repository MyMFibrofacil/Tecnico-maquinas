"""Pruebas unitarias de los extractores documentales."""

from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3
import unittest

from app.extractores.excel import extraer_excel
from app.extractores.imagenes import extraer_imagen
from app.extractores.pdf import extraer_pdf
from app.extractores.sqlite import extraer_sqlite


class ExtractoresTests(unittest.TestCase):
    def test_extrae_pdf(self):
        from reportlab.pdfgen.canvas import Canvas

        with TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "manual.pdf"
            canvas = Canvas(str(ruta))
            canvas.drawString(72, 720, "Alarma del eje A")
            canvas.save()
            contenido, metadata = extraer_pdf(ruta)
            self.assertIn("Alarma del eje A", contenido)
            self.assertEqual(metadata["paginas"], "1")

    def test_extrae_excel(self):
        from openpyxl import Workbook

        with TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "parametros.xlsx"
            libro = Workbook()
            hoja = libro.active
            hoja.title = "Configuración"
            hoja["A1"] = "Eje"
            hoja["B1"] = "A"
            libro.save(ruta)
            contenido, metadata = extraer_excel(ruta)
            self.assertIn("Configuración", contenido)
            self.assertIn("B1=A", contenido)
            self.assertEqual(metadata["hojas"], "1")

    def test_extrae_imagen_sin_ocr(self):
        from PIL import Image

        with TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "placa.png"
            Image.new("RGB", (120, 80), "white").save(ruta)
            contenido, metadata = extraer_imagen(ruta, realizar_ocr=False)
            self.assertIn("Dimensiones: 120 x 80", contenido)
            self.assertEqual(metadata["tipo"], "imagen")

    def test_extrae_sqlite_en_solo_lectura(self):
        with TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "registro.db"
            conexion = sqlite3.connect(ruta)
            conexion.execute("CREATE TABLE alarmas (codigo TEXT, eje TEXT)")
            conexion.execute("INSERT INTO alarmas VALUES ('2905', 'A')")
            conexion.commit()
            conexion.close()
            contenido, metadata = extraer_sqlite(ruta)
            self.assertIn("[Tabla: alarmas]", contenido)
            self.assertIn("2905", contenido)
            self.assertEqual(metadata["tablas"], "1")


if __name__ == "__main__":
    unittest.main()
