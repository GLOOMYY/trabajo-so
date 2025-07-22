# src/simulator.py
import json
from src.process_model import Process, Resource
from src.protocol import apply_ordering


def simulate_scenario(scenario: dict, use_order: bool = False) -> dict:
    """
    Ejecuta una simulación sobre un escenario dado.
    scenario: diccionario con 'processes' (lista de {pid, requests})
    use_order: si se aplica protocolo de orden jerárquico.
    Retorna métricas: deadlocks_detected, avg_latency
    """
    # TODO: implementar simulación
    raise NotImplementedError


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Simulador de deadlocks")
    parser.add_argument("--scenario", required=True,
                        help="Ruta a JSON con definicion de escenarios")
    args = parser.parse_args()
    with open(args.scenario) as f:
        scenarios = json.load(f)
    results = []
    for sid, scenario in scenarios.items():
        res_no = simulate_scenario(scenario, use_order=False)
        res_yes = simulate_scenario(scenario, use_order=True)
        results.append({
            "scenario": sid,
            "deadlocks_without": res_no.get("deadlocks_detected"),
            "deadlocks_with": res_yes.get("deadlocks_detected")
        })
    print(results)

if __name__ == "__main__":
    main()
