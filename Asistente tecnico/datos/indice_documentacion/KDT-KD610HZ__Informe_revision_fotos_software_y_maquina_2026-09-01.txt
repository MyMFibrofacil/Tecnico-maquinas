# Informe de revisión fotográfica

## Máquina

- Fabricante: Guangzhou KDT Machinery Co., Ltd.
- Modelo: KDT KD-610HZ
- Número de serie: 6610220700121
- Fecha de fabricación: 2022/07/09
- Potencia total de placa: 21,9 kW
- Alimentación de placa: 3 fases, 380 V, 50 Hz
- Fecha de las fotografías: 2026/09/01, según los nombres de archivo y el reloj visible en las pantallas.

## Material revisado

- 44 fotografías de pantallas del software.
- 13 fotografías de la máquina y sus conjuntos.
- Las copias de trabajo están en `09_Fotos_Software` y `10_Fotos_Maquina`.

## 1. Software de control

### Identificación visible

En las pantallas aparece:

- Aplicación: `NC boring machine`.
- Versión: `V10.8.4.3`.
- Build: `2023.12.19`.
- Máquina indicada por el software: `610HZ`.
- Interfaz configurada en inglés, con algunos campos internos en chino.
- Usuario visible: `General user`.

La interfaz principal contiene los módulos `Auto`, `Manual`, `Edit`, `Setting`, `Status`, `Maintenance` y `Record`.

### Operación y archivo de trabajo

Las fotos muestran:

- Pantalla manual con representación de los cabezales, mordazas, placas izquierda/derecha, soplado, aspiración y funciones de arranque.
- Controles manuales para los ejes X, A, Y, Z, B, C y U.
- Pantalla de carga/procesamiento de archivos con nombre de pieza, cantidad, dimensiones y rotación.
- Ejemplo visible de pieza de aproximadamente `325 x 582 x 9` y cantidad `3`; este dato pertenece al trabajo fotografiado y no debe tomarse como configuración fija de la máquina.
- Detección opcional de largo, ancho y espesor del panel.
- Lectura de espesor de panel visible en la barra inferior: aproximadamente `40,02` y contador `3382`; debe verificarse si se trata de una lectura actual, un contador o una unidad interna.

### Ejes y posiciones

La barra inferior permite observar velocidad, posición y estado de cada eje. En las fotos se ven, entre otros, valores actuales aproximados:

- X: `1232,70`.
- A: `-2094,69`.
- Y: `813,01`.
- Z: `-197,30`.
- B: `499,99`.
- C: `2,00`.
- U: `-1,01`.

Estos son valores instantáneos de las fotografías, no parámetros de calibración confirmados.

## 2. Parámetros visibles

Las fotografías cubren varias familias de parámetros dentro de `Setting`:

- Configuración automática y manual.
- Parámetros de dispositivo.
- Configuración original.
- Configuración ATC.
- Código de error.
- Configuración del sistema.
- Parámetros de límites.
- Parámetros de procesamiento.
- Parámetros de desbaste/depuración.
- Parámetros de posicionamiento.

Se observan valores asociados a límites de largo, ancho y espesor del panel, alturas mínimas/máximas, compensaciones, posiciones de mordazas, sensores de espesor, tiempos y velocidades. La escala de las fotografías no permite transcribir todos los renglones con seguridad; no deben modificarse basándose únicamente en estas imágenes.

## 3. Entradas y salidas

El software contiene páginas de `Input` y `Output` organizadas por grupos. Las fotos muestran señales relacionadas con:

- Mordazas X y A.
- Placas izquierda y derecha.
- Mesa de rodillos y topes.
- Cabezal de perforación superior e inferior.
- Husillo superior e inferior.
- Aspiración y soplado.
- Presostatos y sensores de seguridad.
- Cambio de herramienta y posicionamiento.
- Electroválvulas de aceite.
- Cilindros y sensores de los conjuntos neumáticos.

Los nombres visibles en pantalla son especialmente útiles para armar una futura tabla de I/O, pero para hacer el listado completo con dirección, borne y módulo sería necesario combinar estas fotos con el esquema eléctrico y la lista oficial de I/O de KDT.

## 4. Servos y ejes

El diagnóstico del software identifica los ejes:

`X`, `A`, `Y`, `Z`, `B`, `C` y `U`.

También se ven pantallas individuales de cada eje con estación, posición objetivo, posición de comando, posición de realimentación y estado de movimiento. En las capturas observadas los campos de conexión muestran estado operativo y códigos de alarma `0x0` en la pantalla de tarjeta, aunque la barra inferior mantiene el aviso `Processing fault`.

Esto confirma funcionalmente la correspondencia de siete ejes que ya figuraba en los esquemas eléctricos. No permite confirmar por sí solo la etiqueta física de cada servodrive.

## 5. Inversores / spindles

El software separa:

- `Upper spindle`.
- `Lower spindle`.

En la pantalla del inversor superior se observa:

- Dirección de comunicación: `5`.
- Frecuencia actual: `0`.
- Frecuencia configurada: `50`.
- Velocidad actual: `0`.
- Estado sin marcha en el momento de la foto.

Esto es consistente con la alimentación de placa de 50 Hz, pero la frecuencia configurada observada no reemplaza la parametrización completa del variador.

## 6. Registros de fallas y alarmas

Las fotos son muy valiosas porque muestran que el equipo conserva históricos en el software.

### Registro general de fallas

Se observa un registro con al menos `4518` eventos acumulados; la pantalla muestra una página de `100` eventos y el indicador `Page 1/46`.

En la página fotografiada aparecen, entre otros:

- Código `37`: falla de comunicación, con descripción parcial legible como `Failure occurs (poor communication, ...)`.
- Código `2905`: `Safety guard is not closed`.
- Código `2701`: `Emergency stop`.
- Código `3000`: alarma de servo.
- Código `2900`: `Low pressure`.

También aparecen eventos repetidos de guarda de seguridad, parada de emergencia y baja presión.

### Registro de inversores

En el histórico del variador superior se observan códigos:

- `OC2`: sobrecorriente durante desaceleración, según la descripción visible.
- `OC3`: sobrecorriente durante velocidad constante, según la descripción visible.
- `OL3`: falla electrónica de sobrecarga, según la descripción visible.
- `SPI`: falla de entrada/fase, según la descripción visible.

Estos registros deben usarse como antecedentes de diagnóstico, no como prueba de una falla presente actualmente.

### Registro de servos

Se observan códigos históricos asociados a ejes:

- `Er21-1`.
- `Er17-1`.
- `Er2-6`.

La foto permite ver que el registro está organizado por eje, pero no alcanza para determinar con seguridad la descripción oficial de cada código. Para eso se necesita el manual específico del servodrive o la tabla oficial de alarmas.

### Registro de tarjetas / comunicación

Una pantalla muestra estaciones identificadas como:

- `X`, `A`, `Y`, `Z`, `B`, `C`, `U`.
- Entradas adicionales `IO-7`, `IO-8`, `IO-9`.

En esa captura se observan códigos de alarma `0x0` y estado de conexión `OP(8)` para las estaciones visibles. También aparece un contador de paquetes transmitidos/recibidos y un paquete erróneo, dato que conviene conservar para futuras comparaciones.

## 7. Estadísticas y registros de operación

El módulo `Record` contiene:

- Vista estadística.
- Registro de procesamiento.
- Estado.
- Estadísticas de datos.
- Registro de fallas.
- Registro de operaciones.
- Información de accesorios.

Las fotos muestran registros con fechas y horas, incluyendo eventos del 2025 y 2026. Esto puede servir para construir una cronología de fallas y mantenimiento, pero las capturas actuales no muestran todo el historial completo.

## 8. Conjuntos físicos fotografiados

Las 13 fotos de la máquina documentan visualmente:

- Área de carga y mesa de trabajo.
- Protecciones y puertas de seguridad.
- Cilindros y elementos neumáticos.
- Cabezal de perforación superior.
- Cabezal de perforación inferior o conjunto opuesto.
- Husillos, motores y carenados.
- Mangueras de aspiración y campanas de polvo.
- Cepillos y faldones de aspiración.
- Guías lineales, cremalleras/cadenas y cadenas portacables.
- Mordazas, topes y apoyos de panel.
- Sensores, electroválvulas y racores neumáticos.
- Conjunto de cambio/soporte de herramientas.
- Tablero o caja auxiliar con módulo electrónico visible.
- Puesto de mando con monitor, teclado y parada de emergencia.

La documentación visual permite relacionar las funciones del software con partes físicas de la máquina. No se debe concluir el modelo exacto de motores, servodrives o válvulas a partir del aspecto exterior.

## 9. Hallazgos importantes

1. La máquina trabaja con siete ejes identificados `X/A/Y/Z/B/C/U`, coincidentes con los esquemas eléctricos.
2. El software ofrece diagnóstico de entradas, salidas, servos e inversores, por lo que puede servir como guía práctica para mantenimiento.
3. La máquina tiene un histórico amplio de fallas; no se trata solamente de alarmas instantáneas.
4. En las capturas se repiten eventos de guarda de seguridad, emergencia, baja presión, comunicación y variador.
5. La barra inferior muestra `Processing fault` en varias pantallas; conviene conservarlo como estado observado, pero no diagnosticar la causa sin una captura de la pantalla de alarma completa y el contexto de operación.
6. Las imágenes no permiten obtener una lista oficial completa de alarmas ni sustituir la documentación KDT.
7. No se desconectó ningún componente para fotografiar etiquetas, por lo que los modelos físicos deben tomarse de los esquemas y manuales ya revisados.

## 10. Próximos documentos útiles

Para cerrar la documentación técnica todavía sería conveniente obtener de KDT:

- Lista oficial de alarmas y descripciones.
- Manual de troubleshooting.
- Lista completa de I/O con direcciones y módulos.
- Tabla oficial de códigos de servos e inversores.
- Respaldo de parámetros y software original.

## Estado del informe

Informe elaborado a partir de las 44 fotos del software y 13 fotos de la máquina guardadas en el expediente de la KDT KD-610HZ. Los valores pequeños o parcialmente ocultos se dejaron como observaciones y no como datos confirmados.
