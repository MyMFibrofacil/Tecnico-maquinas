# Técnico Wpp

Asistente documental para diagnosticar fallas de las máquinas de la fábrica a través de consultas escritas y, posteriormente, WhatsApp.

## Alcance de seguridad

Este proyecto solo consulta documentación y registra casos. No se conecta a las máquinas, no opera el software CNC, no modifica parámetros y no envía comandos de control.

## Estado actual

- Núcleo local funcional para consultas escritas.
- Catálogo multi-máquina.
- Primera máquina configurada: KDT KD-610HZ.
- Búsqueda sobre Markdown, TXT, JSONL, PDF, Excel, fotografías y SQLite mediante un índice documental regenerable.
- Adaptador de WhatsApp preparado como interfaz, sin credenciales ni conexión externa.
- Respuesta breve en formato WhatsApp para casos históricos conocidos.
- Proveedor OpenAI opcional, desactivado si no existe `OPENAI_API_KEY`.

## Ejecución

Desde esta carpeta:

```powershell
python main.py --maquina KDT-KD610HZ --consulta "La máquina muestra Er2-6 en el eje A"
```

Para actualizar el índice documental:

```powershell
python main.py --indexar
```

La indexación lee las fuentes en modo documental. SQLite se abre en solo lectura y las fotografías incorporan metadatos y OCR cuando Tesseract está disponible. El índice se guarda en `datos/indice_documentacion`; las fuentes originales no se modifican.

## Próxima etapa

Validar respuestas con casos reales; luego agregar OpenAI para interpretar lenguaje libre y fotos, y finalmente conectar el adaptador a un proveedor oficial de WhatsApp, manteniendo separado el núcleo técnico.

## Activar análisis visual opcional

Instalar la dependencia definida en `requirements.txt` y configurar `OPENAI_API_KEY` en el entorno local. No guardar la clave en archivos del proyecto ni enviarla por WhatsApp.
