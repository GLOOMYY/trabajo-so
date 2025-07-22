# src/protocol.py
from typing import List, Tuple, Dict

def apply_ordering(requests: List[Tuple[str, str]],
                   resource_order: Dict[str, int]) -> List[Tuple[str, str]]:
    """
    Reordena la lista de peticiones (pid, rid) según el orden jerárquico de recursos.
    requests: lista de tuplas (pid, rid) en el orden original.
    resource_order: mapping rid -> orden (int).
    Retorna la lista ordenada o lanza excepción si hay ciclo.
    """
    # TODO: validar y reordenar
    raise NotImplementedError
