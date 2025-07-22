# Simulador de Prevención de Deadlocks

## 1. ¿Para qué sirve este proyecto?

En entornos concurrentes, los **deadlocks** (interbloqueos) ocurren cuando dos o más procesos quedan bloqueados esperando recursos que nunca se liberan. Este proyecto implementa un **protocolo jerárquico de ordenación de recursos** (“lock ordering”) para **prevenir deadlocks** y compara su comportamiento frente a un sistema que no aplica ninguna política de orden.

* **Lock Ordering**: asigna a cada recurso un “número de orden” global y obliga a todos los procesos a solicitar bloqueos en ese orden ascendente, evitando ciclos de espera.
* **Sin Orden**: los procesos solicitan recursos en el orden que estimen conveniente, lo que puede generar deadlocks.

Además de contar cuántos deadlocks se producen en cada esquema, el simulador mide la **latencia media** de las solicitudes, para evaluar el impacto temporal de aplicar el protocolo.

---

## 2. Ejemplos de uso

### 2.1. Ejecución básica (JSON)

```bash
python -m src.simulator --scenario scenarios.json --metrics
```

Salida:

```json
[
  {
    "scenario": "S1",
    "deadlocks_without": 2,
    "avg_latency_without": 1.50,
    "deadlocks_with": 0,
    "avg_latency_with": 2.00
  },
  {
    "scenario": "S2",
    "deadlocks_without": 3,
    "avg_latency_without": 4.20,
    "deadlocks_with": 0,
    "avg_latency_with": 4.80
  }
]
```

### 2.2. Salida en CSV

```bash
python -m src.simulator --scenario scenarios.json --metrics --output csv > results.csv
```

### 2.3. Modo verbose

```bash
python -m src.simulator --scenario scenarios.json --metrics --verbose
```

Muestra trazas detalladas con timestamps y nivel DEBUG.

---

## 3. Estructura del proyecto

```
deadlock_prevention/
├── src/
│   ├── __init__.py
│   ├── process_model.py   # Clases Process y Resource
│   ├── protocol.py        # apply_ordering con validación
│   └── simulator.py       # CLI avanzado, simulación y métricas
├── tests/
│   ├── __init__.py
│   └── test_simulation.py # pytest: deadlocks, latencia y casos límite
├── scenarios.json         # Ejemplos de escenarios para CLI
├── requirements.txt       # pytest
└── README.md              # Esta documentación
```

---

## 4. Explicación de cada parte del código

### 4.1. `src/process_model.py`

* **`class Resource`**: representa un recurso bloqueable (atributo `rid`).
* **`class Process`**: almacena `pid` y lista `requests` de recursos.

### 4.2. `src/protocol.py`

* **Propósito**: implementar “lock ordering”.
* **`apply_ordering(requests, resource_order)`**:

  1. Valida que cada `rid` exista en `resource_order`, lanza `ValueError` si falta.
  2. Agrupa peticiones por proceso.
  3. Ordena cada lista de recursos según `resource_order[rid]`.
  4. Devuelve lista de tuplas `(pid, rid)` reordenada.

### 4.3. `src/simulator.py`

* **CLI con `argparse`**:

  * `--scenario`: JSON de escenarios.
  * `--verbose`: activa `logger.debug`.
  * `--metrics`: incluye `avg_latency`.
  * `--output`: `json` o `csv`.
* **Logging**: configuración por nivel.
* **`simulate_scenario(...)`**:

  1. Crea objetos `Process`.
  2. Aplana peticiones y, si aplica, llama a `apply_ordering`.
  3. Calcula `avg_latency` como índice medio.
  4. Detecta deadlocks por inversiones de orden entre pares.
  5. Retorna dict con `deadlocks_detected` y `avg_latency`.
* **Salida**: JSON o CSV con métricas sin/con orden.

### 4.4. `scenarios.json`

Define escenarios con:

```json
{
  "S1": {
    "processes": [
      {"pid":"P1","requests":["R1","R2"]},
      {"pid":"P2","requests":["R2","R1"]}
    ],
    "resource_order": {"R1":1,"R2":2}
  },
  ...
}
```

### 4.5. `tests/test_simulation.py`

* Pruebas funcionales de deadlocks y latencia.
* Casos límite:

  * Un solo proceso/petición.
  * Procesos sin recursos en común.
  * Faltan entradas en `resource_order` → `ValueError`.

---
## 5. Salida de ejemplo en CSV

```csv
scenario,deadlocks_without,avg_latency_without,deadlocks_with,avg_latency_with
S1,2,1.50,0,2.00
S2,3,4.20,0,4.80
```

