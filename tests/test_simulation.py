# tests/test_simulation.py
import pytest
from src.simulator import simulate_scenario

@pytest.fixture()
def sample_scenario():
    return {
        'processes': [
            {'pid':'P1','requests':['R1','R2']},
            {'pid':'P2','requests':['R2','R1']}
        ],
        'resource_order':{'R1':1,'R2':2}
    }

def test_deadlock_detected_without_order(sample_scenario):
    res = simulate_scenario(sample_scenario, use_order=False)
    assert res['deadlocks_detected'] >= 1

def test_deadlock_avoided_with_order(sample_scenario):
    res = simulate_scenario(sample_scenario, use_order=True)
    assert res['deadlocks_detected'] == 0
