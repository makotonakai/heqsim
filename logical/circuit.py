from logical.gate import QuantumGate
from device.cluster import QuantumCluster
from device.indexallocator import IndexAllocator
from device.gateallocator import GateAllocator
import numpy as np


class QuantumCircuit:

    def __init__(self, qubit_num):
        self.qubit_num = qubit_num
        self.gate_list = []

        self.cluster = QuantumCluster()
        self.set_index_allocator()
        self.set_gate_allocator()
        self.set_processor_list()

    def x(self, idx):
        self.gate_list.append(QuantumGate("X", idx))

    def y(self, idx):
        self.gate_list.append(QuantumGate("Y", idx))

    def z(self, idx):
        self.gate_list.append(QuantumGate("Z", idx))

    def h(self, idx):
        self.gate_list.append(QuantumGate("H", idx))

    def cx(self, control_idx, target_idx):
        self.gate_list.append(QuantumGate("CNOT", control_idx, target_idx))

    def measure(self, idx):
        self.gate_list.append(QuantumGate("Measure", idx))

    def set_processor_list(self):
        self.processor_list = self.cluster.processor_list

    def set_index_allocator(self):
        self.index_allocator = IndexAllocator(self.qubit_num, self.cluster)

    def set_gate_allocator(self):
        self.gate_allocator = GateAllocator(self.gate_list, self.cluster)

    def allocate_qubits(self):
        self.index_allocator.execute()

    def get_qubit_dict(self):
        qubit_dict = self.index_allocator.get_result()
        return qubit_dict

    def allocate_gates(self):
        qubit_dict = self.get_qubit_dict()
        self.gate_allocator.execute(qubit_dict)

    def run_cluster(self):
        self.cluster.execute()

    def execute(self):
        self.allocate_qubits()
        self.allocate_gates()
        self.run_cluster()

    def state(self, processor):
        return self.cluster.get_state(processor)

    def qubits(self, processor):
        return self.cluster.get_qubit_num(processor)

    def state_str(self, num, digit):
        return bin(num)[2:].zfill(digit)

    def shrink_state_dir(self, state_dir, qubit_num_used):
        new_state_dir = {self.state_str(state, qubit_num_used):
                         1 for state in range(2**qubit_num_used)}
        qubit_num = len(list(state_dir.keys())[0])
        for state in list(new_state_dir.keys()):
            new_state_dir[state] = state_dir[state + '0' * (qubit_num - qubit_num_used)]
        return new_state_dir

    def is_part_of_state(self, indices, state_str, target_state_str):
        total_state_str_shrinked = "".join([target_state_str[index] for index in indices])
        return state_str == total_state_str_shrinked

    def result(self):
        total_state_dir = {self.state_str(state, self.qubit_num): 1 for state in range(2**self.qubit_num)}

        for processor in self.processor_list:
            qubit_num = self.qubits(processor)
            qubit_dict = self.get_qubit_dict()
            qubit_list = qubit_dict[processor]
            qubit_num_used = len(qubit_list)
            state = self.state(processor)
            state_dir = {self.state_str(qubit_idx, qubit_num): state[qubit_idx] for qubit_idx in range(2**qubit_num)}
            state_dir = self.shrink_state_dir(state_dir, qubit_num_used)

            total_states = list(total_state_dir.keys())
            states = list(state_dir.keys())

            for total_state in total_states:
                for each_state in states:
                    if self.is_part_of_state(qubit_list, each_state, total_state):
                        total_state_dir[total_state] *= state_dir[each_state]

        total_state = np.array(list(total_state_dir.values()))
        return total_state
