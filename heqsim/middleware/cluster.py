from heqsim.hardware.processor import QuantumProcessor
from heqsim.hardware.state import QuantumState
from heqsim.middleware.link import Link
from heqsim.middleware.qubitindexmanager import QubitIndexManager
import threading
import time
import os


class QuantumCluster:
    """A class for a cluster of physical quantum processors"""

    def __init__(self):
        """Create a new cluster of quantum processors"""
        self.index_dict = {}
        self.gate_dict = {}
        self.execution_time = 0
        self.network = None

    def prepare_hardware_processor_list(self):
        """Create a list of physical quantum processors"""
        processor_list = self.network.get_processor_list()
        self.hardware_processor_list = []
        for processor in processor_list:
            processor_info = processor.get_info()
            hardware_processor = QuantumProcessor(processor_info)
            self.hardware_processor_list.append(hardware_processor)

    def prepare_quantum_state(self):
        """Create a quantum state"""
        self.total_qubit_num = 0
        processor_list = self.network.get_processor_list()
        for processor in processor_list:
            self.total_qubit_num += processor.qubit_num
        self.total_qubit_num += self.network.get_processor_num()
        self.total_qubit_num += self.network.get_link_num() * 2
        self.quantum_state = QuantumState(self.total_qubit_num)

    def prepare_link_list(self):
        """Create a link list"""
        link_num = self.network.get_link_num()
        self.link_list = [Link() for _ in range(link_num)]

    def get_state(self):
        """Return a quantum state

        Returns:
            ndarray: The statevector of the total quantum state
        """
        return self.quantum_state.vector

    def get_execution_time(self):
        """Return the total execution time

        Returns:
            float: The total execution time (seconds)
        """
        return self.execution_time

    def set_index_dict(self, index_dict):
        """Set the given index dict to this cluster

        Args:
            index_dict (dict): A dict that maps a processor id to the list of indices of allocated qubits
        """
        self.index_dict = index_dict

    def set_gate_dict(self, gate_dict):
        """Set the given gate dict to this cluster

        Args:
            gate_dict (dict): A dict that maps a processor id to the list of allocated quantum gates
        """
        self.gate_dict = gate_dict

    def set_network(self, network):
        """Set the given network to this cluster

        Args:
            network (Network): A network that connects quantum processors
        """
        self.network = network

    def set_quantum_state_to_processor(self, processor, state):
        """Set a particular quantum state to a particular physical quantum processor

        Args:
            processor (QuantumProcessor): A physical quantum processor
            state (QuantumState): A quantum state
        """
        processor.state = state

    def set_gate_list_to_processor(self, processor, gate_list):
        """Set a particular quantum state to a particular physical quantum processor

        Args:
            processor (QuantumProcessor): A physical quantum processor
            state (QuantumState): A quantum state
        """
        processor.gate_list = gate_list

    def set_link_list_to_processor(self, processor, link_list):
        """Set a particular quantum state to a particular physical quantum processor

        Args:
            processor (QuantumProcessor): A physical quantum processor
            state (QuantumState): A quantum state
        """
        processor.link_list = link_list

    def set_lock_to_processor(self, processor, lock):
        """Set a particular quantum state to a particular physical quantum processor

        Args:
            processor (QuantumProcessor): A physical quantum processor
            state (QuantumState): A quantum state
        """
        processor.lock = lock

    def set_qubit_index_manager_to_processor(self, processor, qubit_index_manager):
        """Set a particular quantum state to a particular physical quantum processor

        Args:
            processor (QuantumProcessor): A physical quantum processor
            state (QuantumState): A quantum state
        """
        processor.qubit_index_manager = qubit_index_manager

    def run(self):
        """Execute the simulation of distributed quantum computing"""
        self.prepare_hardware_processor_list()
        self.prepare_quantum_state()
        self.prepare_link_list()

        lock = threading.Lock()
        qubit_index_manager = QubitIndexManager(self.hardware_processor_list, self.network)
        qubit_index_manager.setup()

        for processor in self.hardware_processor_list:
            self.set_quantum_state_to_processor(processor, self.quantum_state)
            self.set_gate_list_to_processor(processor, self.gate_dict[processor.id])
            self.set_link_list_to_processor(processor, self.link_list)
            self.set_lock_to_processor(processor, lock)
            self.set_qubit_index_manager_to_processor(processor, qubit_index_manager)

        # for processor_id in list(self.gate_dict.keys()):
        #     gate_list = self.gate_dict[processor_id]
        #     print("Processor id: ", processor_id)
        #     for gate in gate_list:
        #         print("Name: ", gate.name)
        #         print("Index: ", gate.index)
        #         print("Target index: ", gate.target_index)
        #         if gate.role is not None:
        #             print("Role: ", gate.role)
        #         print()

        time_start = time.time()
        for processor in self.hardware_processor_list:
            processor.start()

        for processor in self.hardware_processor_list:
            processor.join()
        time_end = time.time()

        self.execution_time = time_end - time_start
