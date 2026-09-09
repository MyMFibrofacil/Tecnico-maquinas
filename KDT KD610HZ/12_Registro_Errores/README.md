# Registro histórico de errores — KDT KD-610HZ

Este módulo conserva, de forma acumulativa, cada interacción relacionada con un error de la máquina. El objetivo es construir una base histórica para comparar códigos, ejes, síntomas, condiciones y soluciones confirmadas.

## Archivo principal

- `errores_kdt.jsonl`: un registro JSON por línea, apto para lectura humana y análisis posterior.

## Criterio de registro

Cada nuevo caso debe incluir, cuando esté disponible:

- fecha y origen de la observación;
- código exacto mostrado por la máquina;
- eje, servo, cabezal o componente involucrado;
- posición y estado visibles;
- síntoma informado por el operador;
- evidencia fotográfica o documental;
- diagnóstico confirmado o hipótesis pendiente;
- verificaciones realizadas;
- acción tomada y resultado;
- nivel de confirmación.

Las hipótesis no deben registrarse como fallas confirmadas. Si aparece información nueva, se agrega una actualización al caso original o un nuevo evento relacionado, preservando el historial.

## Uso a futuro

Cada vez que el usuario envíe una interacción sobre un error de la KD-610HZ, se agregará una nueva línea al archivo sin borrar las anteriores. Las fotos definitivas deben guardarse dentro de `09_Fotos_Software` o `10_Fotos_Maquina`, evitando depender de rutas temporales.

