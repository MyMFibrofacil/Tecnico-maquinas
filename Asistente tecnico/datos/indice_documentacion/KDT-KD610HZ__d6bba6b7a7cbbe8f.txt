# Fuentes y estado de descarga

## Archivos descargados

| Archivo | Uso | Fuente |
|---|---|---|
| `01_Maquina/KDT_KD-610HZ_ficha_tecnica_21-9kW.pdf` | Ficha específica de la KD-610HZ | https://www.jacks.co.nz/products/cnc/cnc-drilling/786.pdf |
| `06_Referencias_NoConfirmadas/INVT_SV-DA200/INVT_SV-DA200_manual_oficial.pdf` | Manual anterior de la familia DA200; no es la identificación confirmada | https://www.invt.com/uploads/file1/20200904/DA200%20Series%20Servo%20Drive%20Manual.pdf |
| `06_Referencias_NoConfirmadas/INVT_SV-DA200/INVT_SV-DA200_guia_tecnica_EtherCAT.pdf` | Guía anterior DA200; se conserva como comparación | https://dattech.com.vn/wp-content/uploads/2020/09/DA200-EtherCAT-Technical-Guide.pdf |
| `06_Referencias_NoConfirmadas/INVT_SV-DA200/INVT_DA200_archivo_EtherCAT_XML.rar` | Archivo anterior de identificación EtherCAT; no confirmado para esta máquina | https://www.invt.com/uploads/file1/20221206/DA200%20EtherCAT%20XML%20File.rar |
| `02_Componentes_Electricos/INVT_GD18_manual_oficial.pdf` | Manual del variador Goodrive18 | https://www.invt.com/uploads/file1/20200715/GD18%20Series%20VFD%20Manual.pdf |
| `02_Componentes_Electricos/Delta_R2-EC0902_manual_usuario.pdf` | Manual del módulo remoto EtherCAT 32 DI / 32 DO | https://deltronics.ru/images/manual/R1%2C%20R2/delta-ia-ipc-r2-ec0902-um-en-20210528.pdf |
| `03_Control_y_Programacion/BAZIS-CNC_manual_configuracion_KDT_CNC_Drill.pdf` | Operación y configuración KDT CNC Drill en BAZIS-CNC | https://s3-cold.bazissoft.ru/documentation/en/CNC.pdf |
| `04_Certificados/KDT_KD-610HZ_certificado_CE.pdf` | Certificación CE de la familia KD-610HZ | https://www.list-of-eligible-technologies.com/wp-content/uploads/2023/04/CE-Certificate_KD-610HZ.pdf |
| `01_Maquina/Manual_usuario_KDT_610HZ_escaneado.pdf` | Manual específico de usuario y 48 planos eléctricos | Archivo aportado por el usuario |
| `02_Componentes_Electricos/INVT_SV-DA260/INVT_SV-DA200_DA260_manual_de_familia.pdf` | Manual general de la familia, usado como referencia para DA260 | https://www.invt.com/uploads/file1/20200410/SV-DA200%20Series%20AC%20servo%20drive_V2.2.pdf |
| `02_Componentes_Electricos/INVT_SV-DA260/INVT_SV-DA260_guia_tecnica_EtherCAT.pdf` | Guía EtherCAT DA200/DA260, comunicación y diagnóstico | https://servostar.ru/_uploads/offers/35acb9d2a6/_pdf/SV-DA200%20Series%20AC%20Servo%20Drive%20EtherCAT%20Technical%20Guide_V1.1.pdf |
| `07_Revision_Manual_KDT/Informe_revision_manual_escaneado.md` | Resumen de la revisión, modelos de servos y ubicación de planos | Revisión del manual aportado por el usuario |
| `08_Mantenimiento_Lubricacion/Generico_M_Caseros/Manual_lubricacion_ULTRAFLEX_generico.pdf` | Guía genérica de lubricación y mantenimiento | Archivo aportado por el usuario |

## Referencias consultadas pero no descargadas como manual original

- Página del fabricante KDT con ficha de la máquina: https://en.kdtmac.net/list_34/485.html
- Página rusa de documentación KDT: https://www.kdtmac.ru/dokumentatsiya
- Página específica rusa de la KD-610HZ: https://www.kdtmac.ru/sverlilno-prisadochnyj-centr-s-chpu-kdt-kd-610hz
- Información técnica adicional KDT Bulgaria: https://kdtmac.bg/mashini/%D0%BF%D1%80%D0%BE%D0%B1%D0%B8%D0%B2%D0%BD%D0%B8_%D1%86%D0%B5%D0%BD%D1%82%D1%80%D0%B8/%D0%BF%D1%80%D0%BE%D0%B1%D0%B8%D0%B2%D0%BD%D0%B8_%D1%86%D0%B5%D0%BD%D1%82%D1%8A%D1%80-kd-610hz/
- Página oficial INVT Goodrive18: https://www.invt.com/products/gd18-series-vfd-181
- Página de documentación Delta R2-EC0902: https://deltronics.ru/catalog/kommunikaczionnyie-moduli/r1/dokumentacziya-i-soft/

## Documentación anterior separada

Los documentos anteriores del SV-DA200 quedaron en `06_Referencias_NoConfirmadas/INVT_SV-DA200`. No se consideran la identificación instalada en esta máquina; se conservan únicamente como material comparativo.

## Pendientes prioritarios

1. Conseguir a KDT/M. Caseros el manual de operación, servicio, esquema eléctrico, esquema neumático, lista de alarmas y repuestos correspondientes al **SN 6610220700121**.
2. Confirmar físicamente, cuando sea posible, que los modelos del esquema coinciden con los drives montados.
3. Identificar la computadora o controlador que funciona como EtherCAT master.
