"""Punto de entrada de Técnico Wpp."""

from __future__ import annotations

import argparse
from pathlib import Path

from app.configuracion import cargar_configuracion
from app.repositorios.catalogo_documental import CatalogoDocumental
from app.servicios.asistente_tecnico import AsistenteTecnico
from app.servicios.conversacion_local import ConversacionLocal


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Consulta documental de máquinas de fábrica")
    parser.add_argument("--maquina", help="Código de la máquina, por ejemplo KDT-KD610HZ")
    parser.add_argument("--consulta", help="Consulta técnica escrita")
    parser.add_argument("--conversacion", action="store_true", help="Inicia una sesión conversacional local")
    parser.add_argument("--sesion", help="Reutiliza un identificador de sesión local")
    parser.add_argument("--indexar", action="store_true", help="Reconstruye el índice documental")
    return parser


def main() -> int:
    args = construir_parser().parse_args()
    config = cargar_configuracion(Path(__file__).parent)
    catalogo = CatalogoDocumental(config)

    if args.indexar:
        cantidad = catalogo.reconstruir_indice()
        print(f"Índice actualizado: {cantidad} documentos de texto.")
        return 0

    asistente = AsistenteTecnico(config, catalogo)
    if args.conversacion:
        ConversacionLocal(config, asistente, args.sesion).ejecutar(args.maquina)
        return 0

    if not args.maquina or not args.consulta:
        print("Indique --maquina y --consulta, o use --indexar o --conversacion.")
        return 2
    respuesta = asistente.responder(args.maquina, args.consulta)
    print(respuesta.texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
