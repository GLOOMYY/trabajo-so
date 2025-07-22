# Informe a Fondo: Prevención de Deadlocks en Sistemas Concurrentes

## 1. Introducción

En entornos concurrentes, los **deadlocks** (interbloqueos) ocurren cuando dos o más procesos quedan bloqueados esperando recursos que nunca se liberan, inmovilizando partes críticas del sistema. Este informe explora en profundidad:

* Las **condiciones necesarias** para que ocurra un deadlock.
* **Métodos clásicos** de prevención, evitación y detección/recuperación.
* Detalle del **protocolo de orden jerárquico de locks** (*lock ordering*), su funcionamiento y ventajas.
* **Comparativa** con otros enfoques, destacando por qué *lock ordering* es la mejor opción para nuestro proyecto.
* **Ejemplos reales** de aplicación en bases de datos, sistemas operativos y bibliotecas multihilo.

## 2. Condiciones de Coffman para Deadlocks

Para que se produzca un interbloqueo, deben cumplirse simultáneamente las cuatro condiciones de Coffman:

1. **Exclusión mutua**: un recurso no es compartible; sólo un proceso puede usarlo a la vez.
2. **Retención y espera**: un proceso retiene al menos un recurso y espera por otros.
3. **No preempción**: los recursos no pueden quitarse forzosamente; sólo el dueño los libera.
4. **Espera circular**: existe un ciclo de procesos donde cada uno espera un recurso que posee otro.

Romper una de estas condiciones evita los deadlocks.

## 3. Métodos Clásicos

### 3.1 Prevención

Imponen restricciones para eliminar al menos una condición de Coffman:

* **Eliminar exclusión mutua** (poco práctico en la mayoría de locks).
* **Evitar retención y espera**: solicitar todos los recursos al inicio o liberar antes de pedir otros.
* **Preempción**: forzar liberación de recursos (abortos en transacciones).
* **Espera circular**: imponer un **orden global** de adquisición de recursos.

### 3.2 Evitación

Decidir dinámicamente si conceder un lock para mantener el sistema en un **estado seguro**, p.ej.:

* **Algoritmo del Banquero**: requiere conocer demandas máximas y hace simulaciones de asignación.
* Alto consumo de cómputo y es inviable en sistemas dinámicos.

### 3.3 Detección y Recuperación

Permitir deadlocks ocasionales y luego:

1. **Detectar** ciclos en el grafo de espera.
2. **Recuperar** abortando procesos o preemptando recursos.

* Variante práctica: **timeouts** que abortan tras un tiempo de espera.

## 4. Prevención por Orden Jerárquico de Locks (Lock Ordering)

### 4.1 ¿Cómo Funciona?

1. Asignar a cada recurso un **número de orden** global.
2. Exigir que todos los procesos soliciten locks **en orden ascendente** de dicho número.

Ejemplo:

```txt
F(A) = 1, F(B) = 2
// Todo hilo debe pedir primero A, luego B
```

Con ello, se **elimina la espera circular** por construcción.

### 4.2 Ventajas

* **Garantía determinista** de evitar deadlocks.
* **Bajo overhead** en tiempo de ejecución (sólo disciplina de diseño).
* **Simplicidad conceptual** y aplicabilidad general.
* **Mejor paralelismo** que pedir todos los recursos al inicio.

### 4.3 Desventajas

* Depende de la **disciplina** de los desarrolladores y de la documentación de la jerarquía.
* **Mantenimiento** de la jerarquía al crecer el sistema.
* Menos adecuado si los recursos son muy dinámicos o condicionales.

## 5. Comparativa con Otros Métodos

| Característica         | Banquero (Evitación) | Detección/Recovery        | Lock Ordering (Prevención) |
| ---------------------- | -------------------- | ------------------------- | -------------------------- |
| Costo en ejecución     | Alto (O(m·n²))       | Moderado-alto             | Mínimo                     |
| Conocimiento previo    | Máximas demandas     | No requerido              | Ninguno                    |
| Garantía               | Sí, si condiciones   | No (depende de detección) | Sí, por diseño             |
| Impacto en paralelismo | Medio                | Medio                     | Bajo                       |

## 6. Ejemplos en Sistemas Reales

### 6.1 Base de Datos

* **MySQL/InnoDB**: se recomienda acceder a tablas o filas siempre en un mismo orden para evitar interbloqueos entre transacciones.

### 6.2 Kernel de Linux

* **Lockdep**: herramienta que valida en tiempo de ejecución que ningún módulo adquiera locks fuera del orden definido, evitando deadlocks entre mutexes y spinlocks internos.

### 6.3 Problema de los Filósofos

* Ordenar los palillos (locks) por ID y obligar a cada filósofo a tomar primero el de menor ID y luego el de mayor, eliminando el deadlock clásico.

## 7. Justificación de la Elección

Elegimos **lock ordering** para nuestro proyecto porque:

* Ofrece **ausencia garantizada** de deadlocks sin cálculos en tiempo de ejecución.
* Se ajusta a nuestro **dominio** con recursos conocidos y jerarquía clara.
* Minimiza **overhead** y mantiene **alto paralelismo**.
* Facilita el **debugging** y la documentación clara de la política de locks.