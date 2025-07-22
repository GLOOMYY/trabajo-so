# src/process_model.py
from typing import List

class Resource:
    """
    Representa un recurso identificable por un ID.
    """
    def __init__(self, rid: str):
        self.rid = rid

    def __repr__(self):
        return f"Resource(rid={self.rid})"

class Process:
    """
    Modela un proceso con lista de recursos que solicita.
    """
    def __init__(self, pid: str, requests: List[str]):
        self.pid = pid
        # Lista de IDs de recursos en el orden que los solicita
        self.requests = requests

    def __repr__(self):
        return f"Process(pid={self.pid}, requests={self.requests})"
