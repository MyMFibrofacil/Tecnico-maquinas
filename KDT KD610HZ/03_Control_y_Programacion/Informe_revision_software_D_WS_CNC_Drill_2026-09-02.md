# Informe de revisión del software instalado

## Alcance y cuidado aplicado

Se revisó en modo lectura la carpeta `D:\WS_CNC_Drill`. No se modificó, movió, ejecutó ni eliminó ningún archivo dentro de esa ubicación.

La ruta real accesible en esta sesión fue `D:\WS_CNC_Drill`; la ruta escrita como `D:\WS\_CNC\_Drill` no existe como estructura de carpetas.

## Identificación del paquete

- Aplicación principal: `WS_CNC_Drill.exe`.
- Empresa que figura en la información del ejecutable: Guangzhou Wangshi Software Technology Co., Ltd.
- Versión del ejecutable: `86.2023.1219.2157`.
- Cantidad revisada: 418 archivos.
- El paquete contiene DLL, plugins, recursos de interfaz, bases de datos SQLite, archivos de configuración, logs y un backup ZIP.
- No se encontró código fuente; se trata de una instalación distribuida del software.

## Configuración general

En `hardware.ini` aparece:

- Nombre de máquina: `610HZ`.
- Driver de control: `delta_cat`.
- `noneBackUnload=1`.

En `ZDrillCoreLastInput.json` aparece otra identificación interna: `machine/name = 610Z`. Esta diferencia debe conservarse como observación y no resolverse por suposición; la placa física y el software visible en las fotos identifican la máquina como KD-610HZ / 610HZ.

El archivo `plugins.txt` confirma módulos específicos para:

- Cambio automático de herramientas del spindle.
- Parámetros CAD.
- Base de datos de spindles.
- Configuración de servos.
- Historial de alarmas y registros de máquina.
- Códigos de error.
- Parámetros de máquina, spindles y herramientas.
- Estado de máquina y espera de normalización.

## Bases de datos de parámetros

La carpeta `parameters` contiene 33 bases SQLite con información de operación y configuración. Las más relevantes son:

- `drivers.db`: ejes, nodos y velocidades.
- `inputs.db`: 64 entradas PLC.
- `outputs.db`: 96 salidas PLC.
- `machine.db`: límites, detección de panel, cambio de herramientas y parámetros de proceso.
- `spindles.db`: spindles, herramientas y placas de herramientas.
- `drillPackages.db`: paquetes de perforación, herramientas, presores y orígenes.
- `saws.db`: configuración de sierra.
- `maintain.db`: mantenimiento programado y registros.
- `record.db`: errores, estados, operaciones y uso de herramientas.
- `workError.db`: errores asociados a trabajos, con estados de ejes, entradas y salidas.
- `work.db`: histórico de trabajos procesados.
- `parametersRecord.db`: cambios de parámetros.
- `modbusAddr.db`: direcciones y cola de comunicación.
- `servoAlarmRecord.db`, `masterAlarmRecord.db` y `transducerAlarmRecord.db`: estructuras para alarmas de servos, tarjeta maestra y variadores.

## Ejes y control de movimiento

`drivers.db` contiene siete ejes activos:

| Eje | Prioridad | Tarjeta | Nodo | Velocidad automática | Aceleración | Desaceleración |
|---|---:|---:|---:|---:|---:|---:|
| X | 1 | 0 | 0 | 140500 | 0,2 | 0,25 |
| A | 2 | 0 | 1 | 140500 | 0,2 | 0,25 |
| Y | 3 | 0 | 2 | 90000 | 0,2 | 0,25 |
| Z | 4 | 0 | 3 | 50000 | 0,2 | 0,25 |
| B | 7 | 0 | 4 | 75000 | 0,2 | 0,25 |
| C | 8 | 0 | 5 | 30000 | 0,2 | 0,25 |
| U | 9 | 0 | 6 | 30000 | 0,2 | 0,25 |

Las unidades de velocidad deben confirmarse con el fabricante o el manual del controlador; se conservan aquí tal como están en la base.

Esto refuerza la identificación previa de siete servodrives para X/A/Y/Z/B/C/U.

## Entradas y salidas PLC

### Entradas

La base contiene 64 entradas, distribuidas en los nodos 7, 8 y 9. Entre las señales identificadas aparecen:

- Posiciones de cilindros y presores de los paquetes de perforación.
- Posiciones superior e inferior de ambos spindles.
- Sobrecarga del motor del spindle superior e inferior.
- Inicio listo de paquetes de perforación.
- Fotocélula de medición de largo de panel.
- Posición de mordazas X y A.
- Botón de pedal, inicio y reset.
- Parada de emergencia.
- Baja presión de aire.
- Falta de aceite/grasa de lubricación.
- Puertas y tapas de seguridad.
- Protección por sobrecarga de taladros y ventilador.
- Señal de anomalía del variador.
- Posiciones del palpador de herramientas.
- Confirmaciones de sujeción y liberación de herramientas.

### Salidas

La base contiene 96 salidas. Se identifican, entre otras:

- Expulsión de las 12 herramientas verticales superiores.
- Expulsión de las herramientas TX1, TX2, TY1 y TY2.
- Expulsión de las 9 herramientas inferiores.
- Presores y ruedas de presión.
- Subida y bajada de spindles y sierra.
- Mordazas X y A.
- Cilindros de mesa flotante.
- Electroválvulas de lubricación.
- Arranque de spindle superior, spindle inferior y paquetes de perforación.
- Reset de variador.
- Aspiración, soplado e iluminación.
- Cilindros del cambio de herramienta.

Esta información permite construir una tabla de I/O mucho más completa que la disponible solo en las fotografías, aunque para convertirla en bornes físicos todavía hay que cruzarla con el esquema eléctrico.

## Spindles, perforación y sierra

### Spindles

La base registra dos spindles:

- Spindle superior: ejes Y3/Z4, portaherramienta de 50 mm, posición segura Z 140.
- Spindle inferior: ejes Y7/Z8, portaherramienta de 50 mm, posición segura Z 2.

Ambos tienen parámetros de herramienta, avance, velocidad de entrada y velocidad lineal. La base conserva velocidad de giro de hasta 18000 en los registros principales.

### Paquetes de perforación

- Paquete superior: ejes Y3/Z4, direcciones `1,2,3,4,6`.
- Paquete inferior: ejes Y7/Z8, dirección `5`.

La estructura contiene posiciones de origen, límites, presores, herramientas y distancias de seguridad.

### Sierra

La base registra una sierra superior con espesor de diente de 4 mm, espesor de hoja de 4 mm, radio de herramienta de 60 mm, profundidad de trabajo de 20 mm y velocidad lineal de 8000.

## Herramientas y almacén

La base `spindles.db` contiene 12 herramientas configuradas y 5 placas para el spindle superior. Se identifican:

- `T8`, `T10`, `T12`, `T28`, `T38`, `T7`, `T81`, `T5`.
- `HS8`, `HL8`, `HNM`, `VL8`, `BT8`, `BVL8`.
- `Media Caña`.

La extracción muestra nombres repetidos en distintas estructuras de configuración; por eso el inventario físico debe confirmarse contra la pantalla de herramientas y el almacén real.

Entre los datos técnicos guardados aparecen diámetros, longitudes, longitudes útiles, velocidades de giro, velocidades de entrada, velocidades lineales, profundidades máximas por pasada y distancias seguras.

## Mantenimiento programado

`maintain.db` conserva 14 tareas de mantenimiento y 24 registros de mantenimiento. Entre las instrucciones legibles aparecen:

- Bomba de grasa manual: accionar diariamente 3 a 5 veces antes de comenzar; grasa mecánica 0#.
- Lubricación de bloques y tornillos con aceites indicados por el sistema.
- Engrase semanal de deslizadores no conectados a tubería.
- Limpieza diaria de teclado, pantalla y panel de operación.
- Limpieza semanal de filtros de ventiladores y cajas eléctricas.
- Drenaje diario del tanque de aire.

Estas instrucciones complementan el manual de lubricación ULTRAFLEX, pero antes de convertirlas en una rutina definitiva hay que distinguir las tareas generales del software de las instrucciones específicas de esta unidad.

## Históricos encontrados

El paquete conserva una cantidad importante de datos históricos:

- `record.db`: 1945 errores, 1271 registros de acciones, 2240 registros de estado y 26 registros de herramientas.
- `work.db`: 8532 trabajos registrados, desde 2023-10-25 hasta 2023-12-26 en el campo consultado.
- `workError.db`: 518 errores de trabajos, 1485 registros recientes y 15 muestras.
- `parametersRecord.db`: 1868 cambios de parámetros.
- `modbusAddr.db`: 142062 elementos en la cola `pushQueue`.

### Códigos más repetidos en errores de trabajos

| Código | Cantidad |
|---:|---:|
| 6810 | 210 |
| 3701 | 73 |
| 3503 | 48 |
| 3500 | 44 |
| 3506 | 43 |
| 3504 | 17 |
| 2905 | 17 |
| 3501 | 16 |
| 9031 | 9 |
| 3000 | 9 |
| 3505 | 8 |
| 3502 | 6 |
| 8800 | 4 |
| 2900 | 4 |
| 2701 | 4 |
| 2600 | 3 |
| 7103 | 2 |
| 8801 | 1 |

Los códigos `2905`, `2900`, `2701`, `3000` y `2600` coinciden con la información ya obtenida de las fotografías y de `Error code.xlsx`. El código `6810` es el más frecuente, pero su significado debe consultarse en la tabla de códigos antes de interpretarlo.

En los registros generales recientes aparece repetidamente la parada de emergencia `2701`, almacenada internamente como `急停`. Esto es un dato histórico del paquete y no demuestra por sí solo que la máquina tenga actualmente una falla de emergencia.

## Parámetros particulares detectados

Entre los valores de `machine.db` y el JSON de configuración se observan:

- Largo máximo de panel: 2800.
- Ancho máximo: 1000.
- Espesor máximo: 60.
- Largo mínimo: 70.
- Ancho mínimo: 35.
- Espesor mínimo: 9.
- Detección de largo, ancho y espesor con tolerancia de 2.
- Contador de detección de espesor: 3380 en la base y 3382 visto en las fotos; diferencia que conviene conservar y verificar en la máquina.
- Dirección del variador del spindle superior: 5.
- Dirección guardada del spindle inferior: 6 en `hardware.db`; en otra configuración aparece 0, por lo que se debe confirmar antes de usarla.
- Tipo de variador/transductor: `invt`.
- Comunicación de transductores: 38400 baudios, 8 bits, paridad 2, 1 bit de parada, puerto COM1.
- Cambio automático de herramienta del spindle superior habilitado.
- Cinco posiciones de placa de herramientas configuradas.

## Backup incluido

La carpeta `backup` contiene:

- `20231220091914backup.zip`.

El ZIP incluye bases de parámetros, recursos de interfaz, `hardware.ini` e imágenes de los ejes, herramientas, spindles, ruedas y paquetes de perforación. Es una copia muy valiosa para preservar la configuración de la instalación, pero no se extrajo ni se modificó durante esta revisión.

## Valor para el proyecto técnico

Esta carpeta aporta información que no estaba disponible en los manuales ni en las fotos:

1. Mapeo interno de los siete ejes y sus nodos.
2. Listado de 64 entradas y 96 salidas con nombres funcionales.
3. Parámetros internos de spindles, perforación, sierra y herramientas.
4. Rutinas y frecuencia de mantenimiento registradas por el software.
5. Históricos de errores, trabajos, estados y cambios de parámetros.
6. Configuración de comunicación de variadores y control.
7. Un backup integral de parámetros y recursos de la instalación.

## Próximos pasos recomendados

- Convertir `inputs.db` y `outputs.db` en una tabla técnica bilingüe, cruzada con los planos eléctricos.
- Traducir y clasificar los textos chinos de entradas, salidas y mantenimiento.
- Decodificar los errores históricos `6810`, `3701`, `3503`, `3500`, `3506` y `3504` usando `Error code.xlsx` y los registros del software.
- Convertir los timestamps Unix de los históricos a fecha y hora legibles.
- Comparar los parámetros guardados en la instalación con las fotos actuales y con el backup de 2023.
- Preservar una copia separada del ZIP original antes de cualquier análisis profundo.

## Conclusión

La carpeta `D:\WS_CNC_Drill` es una fuente técnica de alto valor para la KDT KD-610HZ / Flex / Ultraflex. Permite pasar de una documentación descriptiva a un diagnóstico basado en la configuración real del software, sus señales, sus ejes, sus herramientas y sus históricos. La información debe considerarse propia de la instalación revisada y no aplicarse a otra KDT sin comparar modelo y configuración.
