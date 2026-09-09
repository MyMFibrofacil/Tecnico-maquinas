# Proyecto técnico — KDT KD-610HZ

## Identificación de la máquina

- **Marca y modelo:** KDT KD-610HZ
- **Nombres internos / alias:** Flex, Ultraflex
- **Número de serie:** 6610220700121
- **Fecha de fabricación:** 09/07/2022
- **Configuración identificada:** 21,9 kW
- **Dimensiones de referencia:** 5270 × 2660 × 2190 mm
- **Arquitectura de control:** EtherCAT

## Referencia por nombre interno

En el contexto de MyM Fibrofacil S.A., las expresiones **Flex**, **Ultraflex**, **la Flex** y **la Ultraflex** se refieren a esta máquina: **KDT KD-610HZ, número de serie 6610220700121**.

Si una consulta menciona un problema con “la Flex” o “la Ultraflex”, debe asociarse inicialmente con este expediente y con esta máquina. Si el contexto indica otra máquina, se debe pedir confirmación antes de mezclar información.

## Configuración relevada

- 7 servodrives INVT **SV-DA260**, identificados en los planos como **X, A, Y, Z, B, C y U**.
- Modelos según el esquema eléctrico: X/A/B/C/U = **SV-DA260-0R7-4-N0-000H** (0,75 kW); Y/Z = **SV-DA260-1R5-4-N0-000H** (1,5 kW).
- 3 módulos Delta R2-EC0902 EtherCAT, identificados como **RM01, RM02 y RM03**.
- 1 variador INVT Goodrive18, identificado como **VFD01**, con rótulos **UPPER / DOWN**.
- Configuración de fábrica de referencia: 12 brocas verticales superiores, 8 horizontales, 9 inferiores, sierra, spindle superior de 5,5 kW, spindle inferior de 3,5 kW y almacén de 5 herramientas.
- Presión neumática de trabajo de referencia: 0,6 MPa.
- Velocidades de referencia X/Y/Z: 140/90/50 m/min.

## Para qué sirve esta biblioteca

La documentación permite seguir el diagnóstico desde la alarma de KDT hacia EtherCAT, el drive o módulo correspondiente, el código del fabricante y la comprobación física del sensor o actuador.

El manual escaneado de KDT contiene 48 planos eléctricos; las hojas impresas 9 a 15 documentan individualmente los siete servodrives.

## Documentación específica de los servodrives

La carpeta `02_Componentes_Electricos/INVT_SV-DA260` contiene el manual de familia DA200/DA260 y la guía técnica EtherCAT compatible con DA260.

## Software instalado de la máquina

Se revisó en modo lectura la instalación `D:\WS_CNC_Drill`. El informe detallado está en `03_Control_y_Programacion/Informe_revision_software_D_WS_CNC_Drill_2026-09-02.md`. La carpeta original no fue modificada.

La primera guía práctica de diagnóstico está en `03_Control_y_Programacion/Guia_diagnostico_inicial_Flex_Ultraflex.md` y relaciona códigos, subsistemas, entradas/salidas y frecuencia histórica.

## Estado de la documentación KDT propietaria

Se incorporó el documento `01_Maquina/Manual_usuario_operacion_KD610HZ_SM-26-610HZ-EN-01-A1_20220107.pdf`. La revisión está asentada en `01_Maquina/Revision_manual_operacion_KD610HZ_2022.md`. Se considera el manual general de usuario/operación de la familia KD-610HZ y contiene los esquemas neumático y eléctrico, aunque no es un manual exclusivo del número de serie ni un manual detallado del software `WS_CNC_Drill`.

Durante la búsqueda no se localizaron públicamente, para esta máquina y número de serie, los siguientes documentos originales:

- Manual de operación completo.
- Manual de servicio/mantenimiento.
- Esquema eléctrico.
- Esquema neumático.
- Lista de alarmas/troubleshooting de KDT.
- Catálogo completo de repuestos.

La carpeta conserva las referencias web de distribuidores y fabricantes para continuar la búsqueda o solicitar esos documentos a KDT/M. Caseros usando el número de serie.

## Criterio de uso

Los manuales de componentes sirven como documentación técnica de apoyo. Antes de modificar parámetros o cableado hay que confirmar el submodelo exacto instalado y contrastar la información con el esquema de la máquina.
