# Guía de diagnóstico inicial — Flex / Ultraflex

Máquina: **KDT KD-610HZ** — serie **6610220700121**.

Esta guía combina el catálogo de errores extraído del software, las bases SQLite de la instalación, las fotografías de pantalla y el esquema eléctrico. Sirve para orientar la consulta y reunir evidencia; no autoriza a modificar parámetros ni a intervenir un tablero energizado.

## Método de uso

Ante una alarma:

1. Anotar el código exacto y el texto completo.
2. Registrar cuándo aparece: al iniciar, cargar panel, sujetar, medir, perforar, cambiar herramienta o finalizar.
3. Fotografiar la pantalla completa de la alarma y, si es posible, la pantalla de entradas/salidas relacionada.
4. Verificar primero condiciones externas y visibles: panel presente, guarda cerrada, parada de emergencia liberada, presión de aire y herramientas correctamente ubicadas.
5. Comparar el evento con el historial, sin borrar registros.
6. No resetear repetidamente ni cambiar parámetros antes de identificar la causa.

## Alarmas prioritarias

| Código | Descripción del software | Frecuencia en `workError.db` | Área inicial |
|---:|---|---:|---|
| 6810 | Cancel processing | 210 | Operación / cancelación de trabajo |
| 3701 | Waiting for input signal timeout | 73 | Sensor o confirmación de movimiento |
| 3503 | Board is too wide | 48 | Medición de ancho / panel |
| 3500 | No existing panel | 44 | Presencia de panel |
| 3506 | Board is too thin | 43 | Medición de espesor |
| 3504 | Board is too narrow | 17 | Medición de ancho / panel |
| 2905 | Safety guard is not closed | 17 | Guarda de seguridad |
| 3501 | Board detected to be too long | 16 | Medición de largo |
| 9031 | Idle for too long and shutdown | 9 | Inactividad |
| 3000 | Alarma de servo | 9 | Servo / eje |
| 3505 | Board is too thick | 8 | Medición de espesor |
| 3502 | Board is too short | 6 | Medición de largo |
| 8800 | Error al cambiar la herramienta del spindle | 4 | Cambio de herramienta |
| 2900 | Low pressure | 4 | Neumática |
| 2701 | Emergency stop | 4 | Seguridad / emergencia |
| 2600 | Inverter error | 3 | Variador |
| 7103 | Panel is too short | 2 | Control previo de largo |
| 8801 | Hay una herramienta en el spindle; no se permite cambiarla | 1 | Cambio de herramienta |

La frecuencia corresponde a los registros de trabajos encontrados en la instalación, no a una tasa de falla de la máquina. El código `6810` es una cancelación de proceso y no necesariamente una falla técnica.

## 1. Código 37 — comunicación / alarma del driver

**Texto:** `Failure occurs (poor communication, Driver Alm)`.

### Qué indica

El software recibió una condición de comunicación deficiente o una alarma proveniente de un driver.

### Qué revisar sin intervenir el tablero

- Qué eje o dispositivo estaba seleccionado en el momento del evento.
- Si aparece también `3000`, `2901` o un código `Er...` en la pantalla de servos.
- Estado de conexión de la estación correspondiente.
- Si la alarma aparece al habilitar el servo, mover un eje o comenzar un proceso.
- Historial de cambios de parámetros y registros cercanos.

La base de drivers identifica los ejes X, A, Y, Z, B, C y U en nodos 0 a 6 de la tarjeta 0. No se debe concluir qué componente está fallando solo con el código 37.

## 2. Códigos 3000 y 2901 — servo

- `3000`: alarma de servo, texto interno chino `伺服报警`.
- `2901`: error de servo.

### Qué reunir

- Eje indicado: X, A, Y, Z, B, C o U.
- Código específico del servodrive, por ejemplo `Er21-1`, `Er17-1` o `Er2-6`.
- Momento en que aparece y movimiento que se intentaba realizar.
- Estado de posición objetivo, comando y realimentación.
- Si el error se repite en el mismo eje.

La instalación guarda una base `servoAlarmRecord.db`, pero en la copia revisada no contenía registros; los históricos útiles están en `record.db` y `workError.db`.

## 3. Códigos 2600 a 2603 — inversores y spindles

- `2600`: error de inversor.
- `2601`: error del inversor del spindle.
- `2602`: error del inversor del spindle superior.
- `2603`: error del inversor del spindle inferior.

La configuración identifica los inversores de spindle por comunicación: dirección 5 para el spindle superior y dirección 6 para el inferior en `hardware.db`. En las fotos del software se observó el spindle superior con frecuencia actual 0 y frecuencia configurada 50.

### Qué reunir

- Si se trata del spindle superior o inferior.
- Código mostrado directamente en el variador, si la pantalla lo informa.
- Frecuencia actual y configurada.
- Si la alarma aparece al arrancar, durante el trabajo o al detener.
- Si también aparece sobrecarga de cabezal o spindle.

Los códigos propios del variador vistos en las fotografías (`OC2`, `OC3`, `OL3`, `SPI`) deben mantenerse separados de los códigos KDT `2600`–`2603`.

## 4. Seguridad y presión

### `2701`, `2707`, `2708`, `2709`

Son variantes de parada de emergencia o circuito de seguridad:

- `2701`: Emergency stop.
- `2707`: Safety EMG Stop.
- `2708`: Touch screen emergency stop.
- `2709`: Fence gate emergency stop.

### `2904` y `2905`

- `2904`: Safety door is not closed.
- `2905`: Safety guard is not closed.

### `2900`

`Low pressure`.

En `inputs.db` están identificadas señales para parada de emergencia, baja presión, falta de lubricación, puertas/tapas y anomalía del variador. El mapeo funcional visible incluye:

- Nodo 8, puerto 0, bit 8: señal de emergencia.
- Nodo 8, puerto 0, bit 9: alarma de baja presión.
- Nodo 8, puerto 0, bit 10: alarma de aceite/grasa.
- Nodo 8, puerto 0, bit 11: puertas/tapas de seguridad.
- Nodo 8, puerto 0, bit 12: protección por sobrecarga de taladros/ventilador.
- Nodo 8, puerto 0, bit 13: anomalía del variador.

Estas direcciones deben cruzarse con el esquema eléctrico antes de buscar un borne físico.

## 5. Códigos 3500 a 3506 y 7103 — panel

- `3500`: no se detecta panel.
- `3501`: panel demasiado largo.
- `3502`: panel demasiado corto.
- `3503`: panel demasiado ancho.
- `3504`: panel demasiado angosto.
- `3505`: panel demasiado grueso.
- `3506`: panel demasiado fino.
- `7103`: panel demasiado corto en el control previo de largo.

La configuración de la instalación guarda estos límites de referencia:

- Largo: 70 a 2800.
- Ancho: 35 a 1000.
- Espesor: 9 a 60.
- Tolerancia de detección de largo, ancho y espesor: 2.
- Velocidad de detección de largo y ancho: 10000.

Estos valores son parámetros instalados, no necesariamente los límites mecánicos absolutos del modelo. Si el error aparece con un panel que debería estar dentro de rango, hay que comparar el archivo de trabajo, las dimensiones detectadas y la señal del sensor antes de cambiar límites.

## 6. Código 3701 — espera de entrada agotada

**Texto:** `Waiting for input signal timeout`.

Es un código general: el software ordenó una acción y no recibió a tiempo la confirmación esperada. Puede involucrar un cilindro, sensor, mordaza, presor, cabezal, spindle, herramienta, presión o guarda.

### Cómo localizarlo

- Anotar la operación exacta en la que se detuvo.
- Revisar en la pantalla de entradas cuál señal no cambia.
- Buscar el nombre funcional: `enter`, `exit`, `open`, `close`, `ready`, `safe`, `clamp` o `tool`.
- Comparar con el XML de secuencia y con el esquema eléctrico.
- No puentear sensores ni forzar salidas.

## 7. Códigos 8800 y 8801 — cambio de herramienta

- `8800`: el software detecta una inconsistencia entre la herramienta solicitada y el magazine/spindle.
- `8801`: hay una herramienta actualmente en el spindle y no se permite cambiarla.

La instalación tiene cambio automático habilitado para el spindle superior, cinco posiciones de placa y herramientas configuradas como T8, T10, T12, T28, T38, HS8, HL8, HNM, VL8, BT8, BVL8 y Media Caña. Antes de concluir que falta una herramienta, hay que comparar nombre, número, placa y herramienta físicamente instalada.

## 8. Códigos 6810 y 9031

- `6810`: `Cancel processing`; indica cancelación del proceso.
- `9031`: `Idle for too long and shutdown`; apagado por inactividad prolongada.

No deben tratarse automáticamente como fallas de hardware. Conviene conservarlos como eventos operativos y distinguirlos de los códigos que detienen la máquina por seguridad o protección.

## 9. Información disponible para profundizar

La instalación también contiene:

- `workError.db`: error del trabajo con JSON de proceso, código, estado de ejes, entradas y salidas.
- `record.db`: errores, estados y operaciones.
- `parametersRecord.db`: 1868 cambios de parámetros.
- `maintain.db`: tareas y registros de mantenimiento.
- `ZDrillCoreLastInput.json`: última configuración cargada y secuencias de operación.
- `backup\20231220091914backup.zip`: backup de parámetros y recursos.

Con una captura de una alarma concreta se puede buscar el código, consultar su descripción, revisar su frecuencia, asociarlo al subsistema y luego buscar las entradas/salidas esperadas para esa operación.

## Seguridad

Las verificaciones eléctricas, mediciones de tensión, continuidad, desconexión de cables o apertura de tableros deben ser realizadas por personal autorizado y con el procedimiento de bloqueo correspondiente. Esta guía no indica puentear seguridades ni resetear alarmas sin identificar la causa.
