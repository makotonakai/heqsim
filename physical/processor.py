from physical.circuit import PhysicalCircuit
import ray
import sys
import os

@ray.remote
class QuantumProcessor(object):
    
    def __init__(self):
        self.device_name = None
        self.qubit_num = 0
        self.gate_list = []
        self.pc = None

    def set_device_name(self, device_name):
        self.device_name = device_name

    def set_qubit_num(self, qubit_num):
        self.qubit_num = qubit_num

    def set_quantum_circuit(self):
        self.pc = PhysicalCircuit(self.qubit_num)

    def set_gate_list(self, gate_list):
        self.gate_list = gate_list

    def get_state(self):
        return self.pc.state

    def x(self, idx):
        self.pc.px(idx)

    def y(self, idx):
        self.pc.py(idx)

    def z(self, idx):
        self.pc.pz(idx)

    def h(self, idx):
        self.pc.ph(idx)

    def cx(self, control_idx, target_idx):
        self.pc.pcx(control_idx, target_idx)

    