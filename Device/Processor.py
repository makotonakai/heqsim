from Physical.Circuit import PhysicalCircuit
import ray
import sys
import os

@ray.remote
class QuantumProcessor(object):
    
    def __init__(self, device_name, qubit_number, single_qubit_gate_time, two_qubit_gate_time):
        self.device_name = "device"
        self.qubit_number = 0
        self.single_qubit_gate_time = 0
        self.two_qubit_gate_time = 0
        self.index_list = []
        self.gate_lists = []
        self.pc = PhysicalCircuit(self.qubit_number)

    def set_device_name(self, device_name):
        self.device_name = device_name

    def set_qubit_number(self, qubit_number):
        self.qubit_number = qubit_number

    def set_single_qubit_gate_time(self, single_qubit_gate_time):
        self.single_qubit_gate_time = single_qubit_gate_time

    def set_two_qubit_gate_time(self, two_qubit_gate_time):
        self.two_qubit_gate_time = two_qubit_gate_time

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
        string = bin(num)[2:].zfill(self.qubit_number)
        string_list = list(string)
        string_list.insert(new_index, '0')
        new_string = "".join(string_list)
        return new_string

    def add_qubit(self, new_index):
        state_dict = {}
        for idx in range(len(self.pc.state)):
            new_idx = self.add_new_zero(idx, new_index)
            state_dict[new_idx] = self.pc.state[idx]

        new_state = [0 for idx in range(2**(self.qubit_number+1))]
        for key in list(state_dict.keys()):
            new_idx = int(key, 2)
            new_state[new_idx] = state_dict[key]
        self.pc.state = new_state
        return self.pc.state