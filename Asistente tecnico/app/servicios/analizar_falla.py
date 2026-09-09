"""Extrae casos históricos estructurados para evitar mostrar JSON crudo."""

from __future__ import annotations

import json
import re


def extraer_codigo(consulta: str) -> str | None:
    coincidencia = re.search(r"\b(?:(?:er|oc|ol|spi)\s*[0-9]+(?:-[0-9]+)?|[0-9]{4})\b", consulta, re.IGNORECASE)
    return coincidencia.group(0).replace(" ", "") if coincidencia else None


def buscar_caso_historico(documentos, consulta: str) -> dict | None:
    codigo = extraer_codigo(consulta)
    if not codigo:
        return None
    for documento in documentos:
        if documento.ruta.suffix.lower() != ".jsonl":
            continue
        for linea in documento.contenido.splitlines():
            try:
                caso = json.loads(linea)
            except json.JSONDecodeError:
                continue
            if str(caso.get("codigo", "")).lower() == codigo.lower():
                return caso
    return None


def formatear_caso(caso: dict) -> str:
    hipotesis = "\n".join(f"- {item}" for item in caso.get("hipotesis", [])) or "- No registradas."
    verificaciones = "\n".join(f"- {item}" for item in caso.get("verificaciones", [])) or "- Confirmar el código completo y revisar el conjunto asociado."
    return (
        f"Código detectado: {caso.get('codigo', 'sin código')}\n"
        f"Eje: {caso.get('eje', 'no indicado')} | Servo: {caso.get('servo', 'no indicado')}\n"
        f"Estado registrado: {caso.get('estado_visible', 'no indicado')}\n\n"
        f"Diagnóstico: {caso.get('diagnostico', 'pendiente')}\n\n"
        f"Hipótesis registradas:\n{hipotesis}\n\n"
        f"Verificaciones sugeridas:\n{verificaciones}\n\n"
        f"Nivel de confirmación: {caso.get('confirmacion', 'no indicado')}"
    )


def formatear_guia(guia: dict) -> str:
    def lista(clave: str) -> str:
        return "\n".join(f"- {item}" for item in guia.get(clave, [])) or "- No disponible."

    return (
        f"\n\nGuía de diagnóstico — {guia.get('titulo', 'falla detectada')}:\n\n"
        f"Información que debe enviar el empleado:\n{lista('que_pedir')}\n\n"
        f"Verificaciones seguras:\n{lista('verificaciones')}\n\n"
        f"Posibles soluciones, según lo que se confirme:\n{lista('posibles_soluciones')}\n\n"
        f"Límite de la guía: {guia.get('limite', 'la causa debe confirmarse presencialmente.')}"
    )


def formatear_whatsapp(caso: dict, guia: dict | None = None) -> str:
    """Genera una respuesta corta, clara y apta para un empleado."""
    codigo = caso.get("codigo", "sin código")
    eje = caso.get("eje", "no indicado")
    servo = caso.get("servo", "no indicado")
    hipotesis = caso.get("hipotesis", [])
    causas = ", ".join(hipotesis[:3]) if hipotesis else "la causa todavía no está identificada"
    texto = (
        f"Sí. La alarma {codigo} está en el eje {eje}, correspondiente al {servo}.\n\n"
        f"Posibles causas: {causas}.\n\n"
    )
    if guia:
        pedidos = guia.get("que_pedir", [])
        texto += "Primero necesito:\n" + "\n".join(f"- {item}" for item in pedidos[:2]) + "\n\n"
        texto += "No desconectes cables ni abras el tablero con tensión. La causa todavía no está confirmada."
    else:
        texto += "Mandame una foto completa de la alarma y confirmá cuándo aparece. La causa todavía no está confirmada."
    return texto


def formatear_guia_whatsapp(codigo: str, guia: dict) -> str:
    """Genera una respuesta breve cuando existe guía, pero no caso histórico."""
    pedidos = guia.get("que_pedir", [])
    verificaciones = guia.get("verificaciones", [])
    return (
        f"La alarma detectada es {codigo}: {guia.get('titulo', 'falla documentada')}.\n\n"
        f"Primero necesito:\n- {pedidos[0] if pedidos else 'Foto completa de la alarma.'}\n"
        f"- {pedidos[1] if len(pedidos) > 1 else 'Indicar cuándo aparece.'}\n\n"
        "Verificación inicial:\n"
        f"- {verificaciones[0] if verificaciones else 'Mantener la máquina detenida y enviar una foto.'}\n\n"
        f"La causa no está confirmada. {guia.get('limite', '')}"
    )
