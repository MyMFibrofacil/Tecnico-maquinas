# Revisión de `Error code.xlsx`

## Identificación del archivo

- Archivo original: `G:\Mi unidad\Produccion\Maquinas\Flex\Error code.xlsx`.
- Copia incorporada al expediente: `Error_code_KDT_extraido_del_software.xlsx`.
- Hoja: `Sheet1`.
- Rango utilizado: `A1:B604`.
- Columnas: `Error code` y `Error Description`.
- Total: 604 filas incluyendo encabezado, es decir, 603 códigos con descripción.

## Utilidad para la KDT KD-610HZ

El archivo es muy útil. Funciona como una tabla de referencia de alarmas del software y complementa directamente las fotografías de las pantallas de diagnóstico. No parece limitarse a una lista de variadores: incluye errores de control de movimiento, comunicación, ejes, servos, spindles, seguridad, neumática, aspiración y cambio de herramientas.

## Coincidencias con las fotos

El archivo confirma con descripción exacta varias alarmas que aparecían en los registros fotografiados:

| Código | Descripción del archivo |
|---:|---|
| 37 | Failure occurs (poor communication, Driver Alm) |
| 2701 | Emergency stop |
| 2900 | Low pressure |
| 2905 | Safety guard is not closed |
| 3000 | 伺服报警 — alarma de servo |

Esto confirma que el código `37` de las fotos corresponde a una falla de comunicación o alarma del driver, y que los códigos 2701, 2900 y 2905 no son interpretaciones aproximadas.

## Códigos adicionales relevantes

La planilla agrega referencias importantes para el diagnóstico futuro:

- `14`, `30`, `71`, `322`, `323`, `327`, `8401` y `1003008`: servos, señales de alarma, comunicación y movimiento de ejes.
- `33`, `37`, `136`, `316` y `346`: comunicación, red y fallas de enlace.
- `2400` a `2407`: sobrecarga de cabezales, drill heads y drill bags.
- `2500` a `2502`: sobrecarga de spindle superior e inferior.
- `2600` a `2603`: errores de inversor y de inversores de spindle.
- `2701`, `2707`, `2708` y `2709`: parada de emergencia y circuitos de seguridad.
- `2800`, `2801`, `2802` y `2804`: sobrecarga de ventiladores, mesa, transportadores y aspiración.
- `2900`, `2901`, `2902`, `2904` y `2905`: presión, servo, bloque lateral, puerta y guarda de seguridad.
- `3704`: espera por frecuencia del inversor.
- `6906` y `9032`: guarda de seguridad y cortina de seguridad.
- `8404`: condición de seguridad del spindle inferior.
- `8800` a `8806`: cambio de herramienta, magazine y posición del spindle.
- `8810`: dirección de comunicación incorrecta del inversor del spindle.

## Relación con el proyecto

Este archivo permite transformar el registro de alarmas de la máquina en una tabla de diagnóstico con cuatro campos mínimos:

1. Código observado.
2. Descripción oficial del software.
3. Subsistema afectado.
4. Verificaciones recomendadas según el manual y los esquemas.

Por ejemplo, ante el código `2900` se debe revisar el circuito de aire y la presión; ante `2905`, el circuito de guarda; ante `2602`, el inversor del spindle superior; y ante `37`, la comunicación y la alarma del driver. Estas son orientaciones de clasificación, no instrucciones para intervenir eléctricamente sin un técnico.

## Límites

- El archivo no incluye necesariamente la causa física completa ni el procedimiento de reparación.
- No reemplaza el manual de troubleshooting de KDT.
- No se debe asumir que todos los 603 códigos están activos o instalados en esta unidad; la planilla puede contener el catálogo general del software.
- El código `3000` aparece con texto chino, por lo que conviene solicitar a KDT la traducción oficial o la descripción completa.
- Los códigos de variador vistos en las fotos (`OC2`, `OC3`, `OL3`, `SPI`) no aparecen como filas equivalentes en esta tabla; pertenecen al diagnóstico interno del inversor y deben conservarse junto con el manual del Goodrive18.

## Conclusión

El archivo debe conservarse como **fuente principal de consulta de códigos del software KDT**. Aporta descripciones oficiales, confirma las alarmas principales detectadas en las fotos y amplía considerablemente la base para el futuro manual técnico de mantenimiento de la máquina.
