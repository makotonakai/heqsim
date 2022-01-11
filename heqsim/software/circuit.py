from heqsim.software.gate import QuantumGate
from heqsim.middleware.cluster import QuantumCluster
from heqsim.middleware.indexallocator import IndexAllocator
from heqsim.middleware.gateallocator import GateAllocator
import numpy as np


class QuantumCircuit:
    """A class for quantum circuit that a user defines"""

    def __init__(self, qubit_num):
        """Create a quantum circuit

        Args:
            qubit_num (int): A number of qubits in the quantum circuit
        """
        self.qubit_num = qubit_num
        self.gate_list = []

        self.cluster = QuantumCluster()
        self.set_index_allocator()
        self.set_gate_allocator()

    def x(self, index):
        """Add an X gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this X gate is applied to
        """
        self.gate_list.append(QuantumGate("X", index))

    def y(self, index):
        """Add an Y gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this Y gate is applied to
        """
        self.gate_list.append(QuantumGate("Y", index))

    def z(self, index):
        """Add an Z gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this Z gate is applied to
        """
        self.gate_list.append(QuantumGate("Z", index))

    def h(self, index):
        """Add an H gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this H gate is applied to
        """
        self.gate_list.append(QuantumGate("H", index))

    def s(self, index):
        """Add an S gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this S gate is applied to
        """
        self.gate_list.append(QuantumGate("PHASE", index, theta=np.pi / 2))

    def sdag(self, index):
        """Add an S† gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this S† gate is applied to
        """
        self.gate_list.append(QuantumGate("PHASE", index, theta=-np.pi / 2))

    def t(self, index):
        """Add an T gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this T gate is applied to
        """
        self.gate_list.append(QuantumGate("PHASE", index, theta=np.pi / 4))

    def tdag(self, index):
        """Add an T† gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this T† gate is applied to
        """
        self.gate_list.append(QuantumGate("PHASE", index, theta=-np.pi / 4))

    def rx(self, index, theta):
        """Add an Rx gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this Rx gate is applied to
            theta (float): The rotation angle of this Rx gate
        """
        self.gate_list.append(QuantumGate("RX", index, theta=theta))

    def ry(self, index, theta):
        """Add an Ry gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this Ry gate is applied to
            theta (float): The rotation angle of this Ry gate
        """
        self.gate_list.append(QuantumGate("RY", index, theta=theta))

    def rz(self, index, theta):
        """Add an Rz gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this Rz gate is applied to
            theta (float): The rotation angle of this Rz gate
        """
        self.gate_list.append(QuantumGate("RZ", index, theta=theta))

    def phase(self, index, theta):
        """Add an phase gate to this quantum circuit

        Args:
            index (int): The index of the qubit that this phase gate is applied to
            theta (float): The rotation angle of this phase gate
        """
        self.gate_list.append(QuantumGate("PHASE", index, theta=theta))

    def cnot(self, control_index, target_index):
        """Add a CNOT gate to this quantum circuit

        Args:
            control_index (int): The control index of this CNOT gate
            target_index (int): The target index of this CNOT gate
        """
        self.gate_list.append(QuantumGate("CNOT", control_index, target_index))

    def crx(self, control_index, target_index, theta):
        """Add a crx gate to this quantum circuit

        Args:
            control_index (int): The control index of this crx gate
            target_index (int): The target index of this crx gate
            theta (float): The rotation angle of this crx gate
        """
        self.cnot(control_index, target_index)
        self.rx(target_index, theta=theta / 2)
        self.cnot(control_index, target_index)
        self.rx(target_index, theta=theta / 2)

    def cry(self, control_index, target_index, theta):
        """Add a cry gate to this quantum circuit

        Args:
            control_index (int): The control index of this cry gate
            target_index (int): The target index of this cry gate
            theta (float): The rotation angle of this cry gate
        """
        self.cnot(control_index, target_index)
        self.ry(target_index, theta=theta / 2)
        self.cnot(control_index, target_index)
        self.ry(target_index, theta=theta / 2)

    def crz(self, control_index, target_index, theta):
        """Add a crz gate to this quantum circuit

        Args:
            control_index (int): The control index of this crz gate
            target_index (int): The target index of this crz gate
            theta (float): The rotation angle of this crz gate
        """
        self.cnot(control_index, target_index)
        self.rz(target_index, theta=theta / 2)
        self.cnot(control_index, target_index)
        self.rz(target_index, theta=theta / 2)

    def cphase(self, control_index, target_index, theta):
        """Add a cphase gate to this quantum circuit

        Args:
            control_index (int): The control index of this cphase gate
            target_index (int): The target index of this cphase gate
            theta (float): The rotation angle of this cphase gate
        """
        self.phase(control_index, theta=theta / 2)
        self.cnot(control_index, target_index)
        self.phase(target_index, theta=-theta / 2)
        self.cnot(control_index, target_index)
        self.phase(target_index, theta=theta / 2)

    def ccnot(self, control1_index, control2_index, target_index):
        """Add a ccnot gate to this quantum circuit

        Args:
            control1_index (int): The first control index of this crx gate
            control2_index (int): The second control index of this crx gate
            target_index (int): The target index of this crx gate
        """
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
        """Add a measurement operation to this quantum circuit

        Args:
            index (int): The index of the measured qubit
        """
        self.gate_list.append(QuantumGate("Measure", index))

    def set_index_allocator(self):
        """Define a software that allocates qubit indices to all physical quantum processors"""
        self.index_allocator = IndexAllocator(self.qubit_num, self.cluster)

    def set_gate_allocator(self):
        """Define a software that allocates quantum gates to all physical quantum processors"""
        self.gate_allocator = GateAllocator(self.gate_list, self.cluster)

    def allocate_indices(self, network, is_optimized):
        """Execute index allocation

        Args:
            network (Network): A network that quantum processors are connected with
            is_optimized (bool): whether the allocation is optimized
        """
        self.index_allocator.execute(network, self.gate_list, is_optimized)

    def get_index_dict(self):
        """Return the result of index allocation

        Returns:
            dict: A dict that maps each processor id to qubit indices of allocated indices on each processor
                e.g. {0: [1, 2, 3]}
                This means that qubit 1, 2 and 3 are allocated to the physical processor 0
        """
        self.index_dict = self.index_allocator.get_result()
        return self.index_dict

    def allocate_gates(self, network):
        """Execute gate allocation

        Args:
            network (Network): A network that quantum processors are connected with
        """
        index_dict = self.get_index_dict()
        self.gate_allocator.execute(index_dict, network)

    def run_cluster(self):
        """Execute this quantum circuit on the cluster of physical quantum processors"""
        self.cluster.run()

    def set_network_to_cluster(self, network):
        """Apply the given network to the cluster of physical quantum processors

        Args:
            network (Network): A network that quantum processors are connected with
        """
        self.cluster.network = network

    def execute(self, network=None, is_optimized=False):
        """Execute this quantum circuit

        Args:
            network (Network, optional): A network that quantum processors are connected with. Defaults to None.
            is_optimized (bool, optional): whether index alocation is optimized. Defaults to False.
        """
        network.set_node_id()
        self.allocate_indices(network, is_optimized)
        self.allocate_gates(network)
        self.set_network_to_cluster(network)
        self.run_cluster()

    def get_result(self):
        """Retrieve the output of this quantum circuit from the cluster of physical quantum processors

        Returns:
            numpy.array: The statevector of this quantum state
        """
        statevector = self.cluster.get_state()
        # return statevector
        cluster_qubit_num = int(np.log2(len(statevector)))
        original_state = []
        for num in range(2**self.qubit_num):
            index = bin(num)[2:].zfill(self.qubit_num)
            new_index = int(index + "0" * (cluster_qubit_num - self.qubit_num), 2)
            original_state.append(statevector[new_index])
        return original_state

    def get_execution_time(self):
        """Retrieve the total execution time from the cluster of physical quantum processors

        Returns:
            float: The total execution time of this quantum circuit
        """
        execution_time = self.cluster.get_execution_time()
        return execution_time

    def get_gate_dict(self):
        """Return the result of index allocation
        Returns:
            dict: A dict that maps processor id to qubit indices of allocated qubits on each quantum processor
        """
        return self.index_dict
