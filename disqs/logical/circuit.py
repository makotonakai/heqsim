from disqs.logical.gate import QuantumGate
from disqs.device.cluster import QuantumCluster
from disqs.device.indexallocator import IndexAllocator
from disqs.device.gateallocator import GateAllocator
import numpy as np


class QuantumCircuit:

    def __init__(self, qubit_num):
        self.qubit_num = qubit_num
        self.gate_list = []

        self.cluster = QuantumCluster()
        self.set_index_allocator()
        self.set_gate_allocator()

    def x(self, index):
        self.gate_list.append(QuantumGate("X", index))

    def y(self, index):
        self.gate_list.append(QuantumGate("Y", index))

    def z(self, index):
        self.gate_list.append(QuantumGate("Z", index))

    def h(self, index):
        self.gate_list.append(QuantumGate("H", index))

    def cnot(self, control_index, target_index):
        self.gate_list.append(QuantumGate("CNOT", control_index, target_index))

    def measure(self, index):
        self.gate_list.append(QuantumGate("Measure", index))

    def set_index_allocator(self):
        self.index_allocator = IndexAllocator(self.qubit_num, self.cluster)

    def set_gate_allocator(self):
        self.gate_allocator = GateAllocator(self.gate_list, self.cluster)

    def allocate_indices(self, network):
        self.index_allocator.execute(network)

    def get_index_dict(self):
        index_dict = self.index_allocator.get_result()
        return index_dict

    def allocate_gates(self, network):
        index_dict = self.get_index_dict()
        self.gate_allocator.execute(index_dict, network)

    def run_cluster(self):
        self.cluster.run()

    def set_network_to_cluster(self, network):
        self.cluster.network = network

    def execute(self, network=None):
        network.set_node_id()
        self.allocate_indices(network)
        self.allocate_gates(network)
        self.set_network_to_cluster(network)
        self.run_cluster()

    def result(self):
        return self.cluster.quantum_state.vector
