# tests/test_process_model.py
import pytest
from src.process_model import Process, Resource

def test_process_initialization():
    p = Process('P1', ['R1','R2'])
    assert p.pid == 'P1'
    assert p.requests == ['R1','R2']
    assert repr(p) == "Process(pid=P1, requests=['R1', 'R2'])"

def test_resource_initialization():
    r = Resource('R1')
    assert r.rid == 'R1'
    assert repr(r) == 'Resource(rid=R1)'
