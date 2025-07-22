# src/protocol.py
"""
Módulo protocol.py: Implementa el protocolo jerárquico de ordenación de recursos para evitar deadlocks.

Este módulo contiene la función `apply_ordering` que:
  - Recibe una lista de peticiones de recursos como tuplas (pid, rid).
  - Utiliza un diccionario `resource_order` que asigna una prioridad numérica a cada recurso.
  - Valida que todos los recursos solicitados estén definidos en `resource_order`.
  - Reordena, para cada proceso, sus peticiones según la prioridad global, asegurando un orden consistente.

Ejemplo de uso:
    >>> from src.protocol import apply_ordering
    >>> requests = [('P1','R2'),('P1','R1'),('P2','R3')]
    >>> order = {'R1': 1, 'R2': 2, 'R3': 3}
    >>> ordered = apply_ordering(requests, order)
    >>> # ordered == [('P1','R1'),('P1','R2'),('P2','R3')]
"""
from typing import List, Tuple, Dict

def apply_ordering(requests: List[Tuple[str, str]],
                   resource_order: Dict[str, int]) -> List[Tuple[str, str]]:
    """
    Reordena la lista de peticiones (pid, rid) según el orden jerárquico de recursos.

    Parameters:
      - requests: lista de tuplas (pid, rid) indicando qué recursos solicita cada proceso.
      - resource_order: mapping de rid a prioridad numérica (menor = mayor prioridad).

    Returns:
      - Lista de tuplas (pid, rid) ordenada internamente para cada proceso.

    Raises:
      - ValueError: si alguna petición de recurso no está definida en resource_order.
    """
    # Validar recursos solicitados
    missing = {rid for _, rid in requests if rid not in resource_order}
    if missing:
        raise ValueError(f"Los recursos {sorted(missing)} no están en resource_order")

    proc_map: Dict[str, List[str]] = {}
    for pid, rid in requests:
        proc_map.setdefault(pid, []).append(rid)

    ordered: List[Tuple[str, str]] = []
    for pid, rlist in proc_map.items():
        sorted_list = sorted(rlist, key=lambda r: resource_order[r])
        for rid in sorted_list:
            ordered.append((pid, rid))
    return ordered
