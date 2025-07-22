#simulator.py
import json
import sys
import csv
import logging
import sys
import csv
from typing import Dict, List
from src.process_model import Process
from src.protocol import apply_ordering

def simulate_scenario(scenario: Dict, use_order: bool = False) -> Dict:
    """
    Simula un escenario y cuenta deadlocks por inversión de órdenes, además de calcular la latencia media de solicitudes.

    Parameters:
      - scenario: diccionario con:
          * 'processes': lista de dicts {pid: str, requests: [rid,...]}
          * 'resource_order': dict rid -> order_int (opcional si use_order=False)
      - use_order: si es True, aplica `apply_ordering` antes de detectar.

    Returns:
      - Dict con {
          'deadlocks_detected': int,
          'avg_latency': float  # Latencia media basada en índice de ejecución
        }
    """
    procs: List[Process] = [Process(p['pid'], p['requests']) for p in scenario['processes']]
    resource_order = scenario.get('resource_order', {})

    # Aplanar peticiones iniciales
    flat: List[tuple] = [(p.pid, rid) for p in procs for rid in p.requests]
    # Aplicar orden si corresponde
    if use_order:
        flat = apply_ordering(flat, resource_order)

    # Calcular latencia media: índice de cada petición en la lista
    total_requests = len(flat)
    latency_sum = sum(idx for idx, _ in enumerate(flat))
    avg_latency = latency_sum / total_requests if total_requests > 0 else 0.0

    # Reconstruir solicitudes ordenadas por proceso
    proc_reqs: Dict[str, List[str]] = {}
    for pid, rid in flat:
        proc_reqs.setdefault(pid, []).append(rid)

    # Detección de deadlocks por inversiones de orden
    deadlocks = 0
    n = len(procs)
    for i in range(n):
        for j in range(i+1, n):
            p1, p2 = procs[i].pid, procs[j].pid
            req1, req2 = proc_reqs[p1], proc_reqs[p2]
            commons = set(req1) & set(req2)
            for r1 in commons:
                for r2 in commons:
                    if r1 == r2:
                        continue
                    if (req1.index(r1) < req1.index(r2) and req2.index(r1) > req2.index(r2)) or \
                       (req1.index(r1) > req1.index(r2) and req2.index(r1) < req2.index(r2)):
                        deadlocks += 1
                        break
                else:
                    continue
                break
    return {'deadlocks_detected': deadlocks, 'avg_latency': avg_latency}

if __name__ == '__main__':
    import argparse
    from argparse import RawTextHelpFormatter
    import logging
    import json
    import sys
    import csv
    from src.simulator import simulate_scenario

    # --- Argumentos de línea de comandos ---
    parser = argparse.ArgumentParser(
        description='Simulador de deadlocks y métricas de latencia.',
        formatter_class=RawTextHelpFormatter,
        epilog=(
            "Ejemplos de uso:\n"
            "  python -m src.simulator --scenario scenarios.json --metrics\n"
            "  python -m src.simulator --scenario scenarios.json --verbose --output csv"
        )
    )
    parser.add_argument(
        '--scenario', required=True,
        help='Ruta al JSON con definición de escenarios.'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='Muestra detalles de ejecución por escenario.'
    )
    parser.add_argument(
        '--output', choices=['json', 'csv'], default='json',
        help='Formato de salida: json (default) o csv.'
    )
    parser.add_argument(
        '--metrics', action='store_true',
        help='Incluye métricas detalladas por escenario (avg_latency).'
    )
    args = parser.parse_args()

    # --- Configuración de logging ---
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # --- Carga de escenarios ---
    with open(args.scenario, 'r') as f:
        scenarios = json.load(f)

    results = []
    for sid, scenario in scenarios.items():
        try:
            no = simulate_scenario(scenario, use_order=False)
            yes = simulate_scenario(scenario, use_order=True)
        except ValueError as e:
            logger.error(f"[{sid}] Error de validación: {e}")
            results.append({'scenario': sid, 'error': str(e)})
            continue

        # Construir datos de salida
        entry = {
            'scenario': sid,
            'deadlocks_without': no['deadlocks_detected'],
            'deadlocks_with': yes['deadlocks_detected']
        }
        if args.metrics:
            entry['avg_latency_without'] = no['avg_latency']
            entry['avg_latency_with'] = yes['avg_latency']

        results.append(entry)

        # Salida verbose
        if args.verbose:
            logger.debug(
                f"[{sid}] sin orden: {no['deadlocks_detected']} deadlocks, "
                f"latencia={no['avg_latency']:.2f}"
            )
            logger.debug(
                f"[{sid}] con orden: {yes['deadlocks_detected']} deadlocks, "
                f"latencia={yes['avg_latency']:.2f}"
            )

    # --- Emitir resultados ---
    if args.output == 'json':
        print(json.dumps(results, indent=2))
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=results[0].keys())
        writer.writeheader()
        for row in results:
            writer.writerow(row)
