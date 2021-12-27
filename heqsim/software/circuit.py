from heqsim.software.gate import QuantumGate
from heqsim.middleware.cluster import QuantumCluster
from heqsim.middleware.indexallocator import IndexAllocator
from heqsim.middleware.gateallocator import GateAllocator
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

    def s(self, index):
        self.gate_list.append(QuantumGate("PHASE", index, theta=np.pi / 2))

    def sdag(self, index):
        self.gate_list.append(QuantumGate("PHASE", index, theta=-np.pi / 2))

    def t(self, index):
        self.gate_list.append(QuantumGate("PHASE", index, theta=np.pi / 4))

    def tdag(self, index):
        self.gate_list.append(QuantumGate("PHASE", index, theta=-np.pi / 4))

    def rx(self, index, theta):
        self.gate_list.append(QuantumGate("RX", index, theta=theta))

    def ry(self, index, theta):
        self.gate_list.append(QuantumGate("RY", index, theta=theta))

    def rz(self, index, theta):
        self.gate_list.append(QuantumGate("RZ", index, theta=theta))

    def phase(self, index, theta):
        self.gate_list.append(QuantumGate("PHASE", index, theta=theta))

    def cnot(self, control_index, target_index):
        self.gate_list.append(QuantumGate("CNOT", control_index, target_index))

    def crx(self, control_index, target_index, theta):
        self.cnot(control_index, target_index)
        self.rx(target_index, theta=theta / 2)
        self.cnot(control_index, target_index)
        self.rx(target_index, theta=theta / 2)

    def cry(self, control_index, target_index, theta):
        self.cnot(control_index, target_index)
        self.ry(target_index, theta=theta / 2)
        self.cnot(control_index, target_index)
        self.ry(target_index, theta=theta / 2)

    def crz(self, control_index, target_index, theta):
        self.cnot(control_index, target_index)
        self.rz(target_index, theta=theta / 2)
        self.cnot(control_index, target_index)
        self.rz(target_index, theta=theta / 2)

    def cphase(self, control_index, target_index, theta):
        self.phase(control_index, theta=theta / 2)
        self.cnot(control_index, target_index)
        self.phase(target_index, theta=-theta / 2)
        self.cnot(control_index, target_index)
        self.phase(target_index, theta=theta / 2)

    def ccnot(self, control1_index, control2_index, target_index):
        self.h(target_index)
        self.cnot(control2_index, target_index)
        self.tdag(target_index)
        self.cnot(control1_index, target_index)
        self.t(target_index)
        self.cnot(control2_index, target_index)
        self.tdag(target_index)
        self.cnot(control1_index, target_index)
        self.tdag(control2_index)
        self.t(target_index)
        self.cnot(control1_index, control2_index)
        self.h(target_index)
        self.tdag(control2_index)
        self.cnot(control1_index, control2_index)
        self.t(control1_index)
        self.s(control2_index)

    def measure(self, index):
        self.gate_list.append(QuantumGate("Measure", index))

    def set_index_allocator(self):
        self.index_allocator = IndexAllocator(self.qubit_num, self.cluster)

    def set_gate_allocator(self):
        self.gate_allocator = GateAllocator(self.gate_list, self.cluster)

    def allocate_indices(self, network, is_optimized):
        self.index_allocator.execute(network, self.gate_list, is_optimized)

    def get_index_dict(self):
        self.index_dict = self.index_allocator.get_result()
        return self.index_dict

    def allocate_gates(self, network):
        index_dict = self.get_index_dict()
        self.gate_allocator.execute(index_dict, network)

    def run_cluster(self):
        self.cluster.run()

    def set_network_to_cluster(self, network):
        self.cluster.network = network

    def execute(self, network=None, is_optimized=False):
        network.set_node_id()
        self.allocate_indices(network, is_optimized)
        self.allocate_gates(network)
        self.set_network_to_cluster(network)
        self.run_cluster()

    def get_result(self):
        statevector = self.cluster.get_state()
        cluster_qubit_num = int(np.log2(len(statevector)))
        original_state = []
        for num in range(2**self.qubit_num):
            index = bin(num)[2:].zfill(self.qubit_num)
            new_index = int(index + "0" * (cluster_qubit_num - self.qubit_num), 2)
            original_state.append(statevector[new_index])
        return original_state

    def get_execution_time(self):
        execution_time = self.cluster.get_execution_time()
        return execution_time

    def get_gate_dict(self):
        return self.index_dict
