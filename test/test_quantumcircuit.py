from heqsim.logical.circuit import QuantumCircuit
from heqsim.logical.gate import QuantumGate
import unittest


class TestQuantumCircuit(unittest.TestCase):

    def test_gate_list(self):

        qc = QuantumCircuit(1)
        qc.x(0)

        expected_gate_name = "X"
        expected_gate_index = 0

        gate = qc.gate_list[0]
        assert gate.name == expected_gate_name
        assert gate.index == expected_gate_index
