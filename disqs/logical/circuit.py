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
        self.set_processor_list()

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

    def set_processor_list(self):
        self.processor_list = self.cluster.processor_list

    def set_index_allocator(self):
        self.index_allocator = IndexAllocator(self.qubit_num, self.cluster)

    def set_gate_allocator(self):
        self.gate_allocator = GateAllocator(self.gate_list, self.cluster)

    def allocate_qubits(self, network):
        self.index_allocator.execute(network)

    def get_qubit_dict(self):
        qubit_dict = self.index_allocator.get_result()
        return qubit_dict

    def allocate_gates(self, network):
        qubit_dict = self.get_qubit_dict()
        self.gate_allocator.execute(qubit_dict, network)

    def run_cluster(self):
        self.cluster.run()

    def execute(self, network=None):
        network.set_node_id()
        self.allocate_qubits(network)
        self.allocate_gates(network)
        self.run_cluster()

    def state(self, processor):
        return self.cluster.get_state(processor)

    def qubits(self, processor):
        return self.cluster.get_qubit_num(processor)

    def result(self):
        return self.cluster.state.vector
