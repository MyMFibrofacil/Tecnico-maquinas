# Análisis del programa Albatros del router KDT KN-3710H

Fecha de revisión: 2026-09-09  
Fuente principal: copia de `E:\Albatros` tomada del Router Nuevo KN-3710H.

## Alcance

Este documento reconstruye el funcionamiento del entorno Albatros/Tpa utilizado por el router. Se revisaron ejecutables, configuración, PLC, base de herramientas, outfit, archivos de bancada, logs y manuales incluidos en la copia.

La revisión es de solo lectura. No se modificaron archivos, parámetros, registro de Windows ni conexiones de la máquina.

## Arquitectura funcional

### TpaCAD

Es el editor CAD/CAM. Permite crear o importar una pieza, trabajar sobre sus caras, agregar operaciones, asignar tecnología y generar el programa de mecanizado.

Archivos y componentes relacionados:

- `Bin\Tpacad.exe`
- `Bin\TpaSpa.Cad*.v2.dll`
- `Bin\TpaSpa.Dxf*.v2.dll`
- `Bin\TpaSpa.PzaToTpa.dll`
- `TpaCadCfg\CUSTOM\TPACAD.xml`
- `Product\` para productos y programas guardados

### TecnoManager

Es el módulo de parametrización tecnológica. Administra las herramientas, el outfit, la bancada, los rieles, las ventosas, los correctores y los parámetros del cambiador.

Archivos y componentes relacionados:

- `Bin\TecnoManager.exe`
- `System\Tecno\TOOLDATA.XML`
- `System\Tecno\OUTFDATA.XML`
- `System\Tecno\TECDATA.XML`
- `System\Tecno\TOOLTECNO.XML`
- `System\Tecno\TOOLTREE.XML`
- `System\Tecno\BUSHCFG.xml`
- `TpaCadCfg\CUSTOM\TPACAD.xml`

### WSC/WSCM

Es el entorno de operación y ejecución. Recibe programas, forma listas de trabajo, muestra la bancada, permite posicionar rieles y ventosas, verifica la lista y simula el ciclo.

Archivos y componentes relacionados:

- `Bin\WSCM.exe`
- `Bin\TpaSpa.CncBoard*.v2.dll`
- `Bin\COM_CncBoard.dll`
- `System\Wsc\DBConf.xml`
- `System\Wsc\DefList.xml`
- `System\Wsc\CncBoardSettings.XML`
- `System\Wsc\CncBoard_Dock_Layout.xml`
- `Tmp\CncBoard_mod0.log`
- `Tmp\CncBoard_dev_mod0.log`

### Albatros y PLC

Es la capa de control que comunica la interfaz con el módulo de máquina y sus dispositivos.

Archivos principales:

- `Bin\Albatros.exe`
- `Bin\CncTpa.exe`
- `Bin\TpaSock.exe`
- `Bin\AlbDhcp.exe`
- `MOD.0\CONFIG\MXMAC.BIN`
- `MOD.0\Plc\MAIN.sfun`
- `MOD.0\Plc\BENCH.sfun`
- `MOD.0\Plc\CNCBOARD.clib`
- `MOD.0\Plc\DEVICES.sfun`
- `MOD.0\Plc\EMERGENCY.sfun`
- `MOD.0\Plc\SPINDLE.sfun`
- `MOD.0\Plc\TOOLSMAG1.sfun`
- `MOD.0\Plc\INVERTER_MODBUS.sfun`

## Flujo operativo reconstruido

1. En TpaCAD se crea o importa el programa.
2. Se define la pieza, la cara y las operaciones.
3. Cada operación recibe una herramienta y parámetros tecnológicos.
4. TecnoManager resuelve la herramienta contra la base y el outfit.
5. WSC recibe el programa y lo incorpora a una lista de ejecución.
6. Se configura o revisa la posición de rieles, ventosas y pieza.
7. Se ejecuta `Verify List` para revisar la lista.
8. Se ejecuta `Simulation` para comprobar la secuencia sin mecanizar.
9. Se revisan ejes, mensajes, errores de ciclo y dispositivos.
10. Solo después de esas verificaciones se inicia el ciclo real.

## Versiones encontradas

### Ejecutables

- `Albatros.exe`: 3.2.0.90
- `Tpacad.exe`: 2.2.10.0
- `TecnoManager.exe`: 1.28.0.0
- `WSCM.exe`: 6.2.0.0
- `Nesting.exe`: 3.10.2.0
- `CncTpa.exe`: 3.2.0.26
- `TpaSock.exe`: 1.5.24

### Parámetros declarados

`TECDATA.XML` declara:

- Software: `WSCM 3.6`
- Firmware: `Albatros 3.1 Sp1`
- Fecha declarada: `14/01/2013`

La diferencia entre esos valores históricos y los ejecutables actuales no prueba una falla. Indica que el archivo de parámetros conserva una identificación antigua y debe compararse con la pantalla real de versión del router.

## Herramientas y outfit

### Outfit activo

`OUTFDATA.XML` contiene un único outfit:

- Descripción: `GP13`
- Grupo: `1`

Posiciones observadas:

| Posición | Nombre configurado |
|---:|---|
| 1 | MECHA 4MM |
| 2 | MECHA 15 |
| 3 | 5mm |
| 4 | 8mm |
| 5 | 8mm |
| 6 | 5mm |
| 7 | 7mm |
| 8 | 8mm |
| 9 | 35mm |
| 10 | 8mm |
| 11 | 8mm |
| 12 | 8mm |
| 41 | UtD8F3 |
| 42 | UtD8F5 |
| 51 | UtD8F4 |
| 52 | UtD8F6 |
| 53 | UtD8F4 |
| 54 | UtD8F6 |
| 111 | Fresa 16mm |
| 112 | Fresa 12mm |
| 113 | Fresa de 28mm |
| 114 | Fresa 18.5m |
| 115 | Fresa 10mm |
| 116 | Fresa 4mm |
| 117 | Fresa Dibujo |
| 118 | Fresa redonda |
| 119 | Fresa 8mm |
| 120 | fresa de 6mm |

### Base de herramientas

`TOOLDATA.XML` contiene 30 registros. Dieciséis tienen un ID distinto de cero.

Los IDs activos observados son:

`1000`, `1009`, `1010`, `1011`, `1012`, `1013`, `1014`, `1015`, `1016`, `1017`, `1018`, `1019`, `1020`, `1021`, `1022` y `1200`.

La herramienta `1012` tiene diámetro 12 mm, largo aproximado 109,725 mm y largo de trabajo 25 mm. Esto coincide por diámetro con la herramienta denominada `Fresa 12mm` en la posición 112.

La coincidencia es técnicamente útil, pero no debe interpretarse como prueba de que el ID 1012 sea la posición 112: el ID y la posición física son campos independientes.

### Cambiador declarado en TECDATA

`TECDATA.XML` contiene tres grupos de cambiador:

| Grupo | Tipo | Cantidad declarada | Fulcro / separación |
|---:|---:|---:|---|
| 1 | 2 | 12 | X=0, Y=0, Delta X=120 |
| 2 | 1 | 6 | X=200, Y=-200, Delta Y=50 |
| 3 | 2 | 8 | X=32, Y=-250, Delta X=140 |

Existe una diferencia que debe verificarse en la máquina: el outfit muestra diez posiciones entre 111 y 120, mientras que uno de los grupos de `TECDATA.XML` declara ocho posiciones. No se recomienda editar este dato sin comparar primero la pantalla real de TecnoManager y la distribución física.

## Bancada y dispositivos

`DBConf.xml` define, entre otros, los ejes `X`, `Y`, `Z`, `X1`, `B` y `C`.

También aparecen dispositivos y variables relacionados con:

- `EMERG.PowerOk`
- `INVERTER.InverterInRun`
- `INVERTER.VOut`
- `DriveReset`
- `cmdManulaToolChanger`
- `resetAutoToolChange`
- `BENCH.MiddleParkingPosition`
- `TESTA.UtMont`
- `g_Manual_Loading`

Esto confirma que la interfaz WSC no es solamente un visor: también está vinculada al estado de dispositivos y al control de movimientos. Las pruebas de movimiento deben hacerse exclusivamente con el operador frente a la máquina y con el procedimiento de seguridad correspondiente.

`CncBoardSettings.XML` indica:

- Comunicación de red habilitada.
- Modo offline deshabilitado.
- Simulación deshabilitada como modo permanente.
- Verificación de lista disponible.
- Vista de bancada, rieles, topes y paneles habilitada.
- Cambio automático de herramientas disponible desde la interfaz.

`Bin\\tpa.ini` agrega datos relevantes:

- `Language=ESP`.
- `OffLine=0`.
- `Simulation=0`.
- `HwClipper=1`.
- `Editor=1`.
- `CustomElab=1`.
- `ToolByPosition=0`.
- `debug=1`.
- Verificación de parámetros, variables globales y funciones activada.

`ToolByPosition=0` es especialmente importante: no se debe asumir que el número de posición física del cargador sea el identificador que el programa espera. La herramienta debe analizarse primero por su ID y luego por su asignación física dentro del outfit.

`ConfTecnoManager.xml` declara las cuatro pestañas principales sin protección ni deshabilitación (`Tab_1_Protected` a `Tab_4_Protected` y `Tab_1_Disabled` a `Tab_4_Disabled` en cero). Esto facilita la consulta del sistema, pero aumenta el riesgo de modificar accidentalmente herramientas, outfit, bancada o parámetros tecnológicos. En el router real cualquier modificación debe hacerse únicamente con respaldo previo y procedimiento controlado.

## Comunicación

`DBDhcp.txt` contiene el registro:

```text
TPACEF6222,172.16.2.10,00-07-32-53-41-E3,1788810869
```

`System\Connection.bat` ejecuta:

```text
c:\albatros\bin\albdhcp.exe /i
```

Esto confirma que la instalación original espera ejecutarse en `C:\Albatros` y que la comunicación depende del servicio o componente `AlbDhcp`.

La copia de `E:\Albatros` no debe ejecutarse como si fuera una instalación independiente: conserva rutas absolutas a `C:\Albatros`, componentes registrados de Windows y posibles dependencias de red del router.

## Componentes faltantes o dudosos

El `install.log` registra intentos fallidos de registrar:

- `AlbGeos.dll`
- `CncCad32.dll`
- `CPanEdi32.dll`
- `EdiLicObj.dll`
- `SysObj.dll`
- `DataWork.ocx`

Ninguno de esos archivos aparece en la copia, y `tpa.ini` referencia directamente:

```text
C:\Albatros\Bin\SysObj.dll
```

`SysObj.dll` debe revisarse directamente en el router. Su ausencia en la copia puede deberse a que la copia no fue completa, a que el archivo estaba fuera de la carpeta o a que pertenece a una instalación anterior. No debe restaurarse ni reemplazarse automáticamente sin comparar con el router original.

También hay un XML inválido:

```text
TpaCadCfg\CUSTOM\CADAUX_ENG.xmlng
```

El error está en el atributo `longName` de la primera línea de idioma. Puede afectar la carga del idioma inglés, pero no parece afectar el funcionamiento en español.

## Logs revisados

- `Tmp\CncBoard_mod0.log`: contiene actividad de listas, estados de máquina, mensajes de ejecución y comandos de limpieza de errores.
- `Tmp\CncBoard_dev_mod0.log`: contiene cambios de estado de dispositivos del módulo 0.
- `Tmp\CncBoard Timing.log`: registra una inicialización de CncBoard de aproximadamente 8,9 segundos.
- `TpaCadCfg\LOGS\TPACAD-1.LOG`: registra arranques y cierres normales de TpaCAD.
- `Tmp\ErrGPL.txt`: indica `Ningún error`.

Los mensajes `VAL_CLEARSYSTEMERROR` del log de CncBoard prueban que se limpiaron estados de error, pero no permiten saber por sí solos cuál fue el error físico original.

## Procedimiento de diagnóstico que usaré en adelante

## Procedimientos operativos de consulta

### Revisar una herramienta sin modificarla

1. Abrir TecnoManager.
2. Entrar en la pestaña de base de herramientas.
3. Seleccionar la herramienta por ID o por sus características.
4. Leer diámetro, largo, tipo, cara, largo útil y correctores.
5. No utilizar `Save` después de una consulta.

### Revisar el outfit

1. Entrar en `Outfit parameters`.
2. Seleccionar el outfit `GP13`.
3. Identificar el grupo y el bush/posición.
4. Comparar el nombre de la herramienta con `OUTFDATA.XML`.
5. Confirmar la herramienta en `TOOLDATA.XML`.
6. No arrastrar herramientas ni guardar cambios durante el diagnóstico.

### Revisar bancada y ventosas

1. Entrar en `Bench parameters`.
2. Consultar primero parámetros generales.
3. Revisar cantidad y tipo de rieles.
4. Revisar tipos y límites de ventosas.
5. Revisar la configuración del plano o grid.
6. Comparar la representación gráfica con la bancada física.

### Revisar parámetros tecnológicos

1. Entrar en `Technological parameters`.
2. Consultar parámetros generales de máquina.
3. Consultar coordenadas en el aire.
4. Consultar avances de trabajo y penetración.
5. Consultar correctores de spindle y grupos.
6. Consultar parámetros del cambio de herramienta.
7. No modificar offsets, velocidades, límites ni posiciones sin respaldo y validación física.

### Verificar una lista en WSC

1. Abrir o cargar la lista.
2. Confirmar los nombres de los programas.
3. Confirmar habilitación de cada línea.
4. Revisar parámetros de pieza y repetición.
5. Revisar rieles y ventosas en la vista de bancada.
6. Ejecutar `Verify List`.
7. Ejecutar `Simulation`.
8. Revisar la ventana de mensajes, errores de ciclo y errores de sistema.
9. No presionar `Start` hasta terminar todas las comprobaciones.

### Revisar un programa en TpaCAD

1. Abrir el archivo sin sobrescribir el original.
2. Confirmar dimensiones de la pieza.
3. Confirmar la cara de aplicación.
4. Revisar operaciones y herramientas.
5. Revisar la vista 2D y 3D.
6. Compilar o verificar el programa.
7. Revisar errores de herramienta, geometría, parámetros y tecnología.
8. Guardar una copia separada si se necesita experimentar.

### Herramienta no reconocida

1. Leer el ID exacto mostrado por el programa.
2. Revisar si el ID existe en `TOOLDATA.XML`.
3. Revisar diámetro, largo, tipo y cara de trabajo.
4. Revisar el outfit `GP13`.
5. Revisar la posición física asignada.
6. Verificar si la herramienta está disponible en el grupo correcto.
7. Ejecutar verificación y simulación.
8. Recién después revisar el `.TCN`.

### Programa que no ejecuta

1. Confirmar que el programa abre en TpaCAD.
2. Revisar errores de compilación.
3. Confirmar herramienta y cara.
4. Revisar la lista WSC.
5. Ejecutar `Verify List`.
6. Ejecutar `Simulation`.
7. Revisar errores de ciclo y mensajes de sistema.
8. Revisar bancada, pieza, rieles y ventosas.
9. Revisar comunicación y estado del PLC.

### Falla de comunicación

1. Confirmar que el router está en la red de máquina.
2. Confirmar IP, nombre y MAC de la controladora.
3. Confirmar que `AlbDhcp` está iniciado.
4. Confirmar que WSC no está en modo offline.
5. Revisar `CncBoard_mod0.log` y `CncBoard_dev_mod0.log`.
6. Separar una falla de software de una falla de PLC, EtherCAT, variador o módulo de E/S.

## Estado del análisis

### Confirmado por archivos

- La copia contiene el entorno principal de Albatros/TpaCAD/WSC.
- La configuración corresponde a una máquina CNC con ejes, bancada, herramientas, cambiador e inversor.
- Existe un outfit real con herramientas de perforado y fresado.
- La comunicación de red está habilitada en la configuración.
- Hay registros de operación recientes.
- La copia fue tomada de un sistema que estaba siendo utilizado.

### Pendiente de confirmar en el router encendido

- Existencia de `C:\Albatros\Bin\SysObj.dll`.
- Registro de OCX/DLL en Windows.
- Versión efectiva mostrada por Albatros y WSCM.
- Correspondencia física entre posiciones 111-120 y el cambiador.
- Estado real de la IP `172.16.2.10`.
- Compilación y carga efectiva del PLC.
- Comunicación con ejes, inversor, spindle, vacío y cambiador.
- Prueba completa de un programa en simulación y luego en ciclo controlado.

## Regla de seguridad

La copia permite comprender y diagnosticar el software, pero no permite afirmar que un parámetro sea seguro para modificar en la máquina. Todo cambio de herramienta, corrector, bancada, cambiador, PLC o comunicación debe respaldarse y validarse con el router detenido, el procedimiento de seguridad correspondiente y el operador controlando físicamente la máquina.
