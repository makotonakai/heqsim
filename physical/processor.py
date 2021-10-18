from physical.circuit import PhysicalCircuit
import ray
import sys
import os

@ray.remote
class QuantumProcessor(object):
    
    def __init__(self):
        self.device_name = None
        self.qubit_num = 0
        self.index_list = []
        self.gate_lists = []
        self.pc = None

    def set_device_name(self, device_name):
        self.device_name = device_name

    def set_qubit_num(self, qubit_num):
        self.qubit_num = qubit_num

    def set_quantum_circuit(self):
        self.pc = PhysicalCircuit(self.qubit_num)

    def get_device_name(self):
        return self.device_name

    def get_qubit_num(self):
        return self.qubit_num

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

    def add_new_zero(self, num, new_index):
        string = bin(num)[2:].zfill(self.qubit_num)
        string_list = list(string)
        string_list.insert(new_index, '0')
        new_string = "".join(string_list)
        return new_string

    def add_qubit(self, new_index):
        state_dict = {}
        for idx in range(len(self.pc.state)):
            new_idx = self.add_new_zero(idx, new_index)
            state_dict[new_idx] = self.pc.state[idx]

        new_state = [0 for idx in range(2**(self.qubit_num+1))]
        for key in list(state_dict.keys()):
            new_idx = int(key, 2)
            new_state[new_idx] = state_dict[key]
        self.pc.state = new_state
        return self.pc.state