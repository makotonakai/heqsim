from heqsim.hardware.processor import QuantumProcessor
from heqsim.hardware.state import QuantumState
from heqsim.middleware.link import Link
from heqsim.middleware.connectionmanager import ConnectionManager
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

    def create_physical_processor_list(self):
        """Create a list of physical quantum processors"""
        physical_processor_list = []
        processor_list = self.network.get_processor_list()
        for processor in processor_list:
            processor_info = processor.get_info()
            physical_processor = QuantumProcessor(processor_info)
            physical_processor_list.append(physical_processor)
        return physical_processor_list

    def create_quantum_state(self):
        """Create a quantum state"""
        processor_list = self.network.get_processor_list()
        total_qubit_num = 0
        for processor in processor_list:
            total_qubit_num += (processor.qubit_num + 2)
        return QuantumState(total_qubit_num)

    def create_link_list(self):
        """Create a link list"""
        link_num = self.network.get_link_num()
        link_list = [Link() for _ in range(link_num)]
        return link_list

    def create_connection_manager(self):
        """Create a connection manager"""
        processor_list = self.network.get_processor_list()
        connection_manager = ConnectionManager(processor_list)
        connection_manager.initialize()
        return connection_manager

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
            gate_list (list): The list of quantum gates
        """
        processor.gate_list = gate_list

    def set_link_list_to_processor(self, processor, link_list):
        """Set a particular quantum state to a particular physical quantum processor

        Args:
            processor (QuantumProcessor): A physical quantum processor
            link_list (list): The list of communication links
        """
        processor.link_list = link_list

    def set_lock_to_processor(self, processor, lock):
        """Set a particular quantum state to a particular physical quantum processor

        Args:
            processor (QuantumProcessor): A physical quantum processor
            state (QuantumState): A quantum state
        """
        processor.lock = lock

    def set_connection_manager_to_processor(self, processor, connection_manager):
        """Set a particular quantum state to a particular physical quantum processor

        Args:
            processor (QuantumProcessor): A physical quantum processor
             (QuantumState): A quantum state
        """
        processor.connection_manager = connection_manager

    def run(self):
        """Execute the simulation of distributed quantum computing"""

        self.physical_processor_list = self.create_physical_processor_list()
        self.quantum_state = self.create_quantum_state()
        self.link_list = self.create_link_list()
        self.connection_manager = self.create_connection_manager()
        self.lock = threading.Lock()

        for processor in self.physical_processor_list:
            self.set_quantum_state_to_processor(processor, self.quantum_state)
            self.set_gate_list_to_processor(processor, self.gate_dict[processor.id])
            self.set_link_list_to_processor(processor, self.link_list)
            self.set_lock_to_processor(processor, self.lock)
            self.set_connection_manager_to_processor(processor, self.connection_manager)

        # for processor_id in list(self.gate_dict.keys()):
        #     gate_list = self.gate_dict[processor_id]
        #     print("Processor id: ", processor_id)
        #     for gate in gate_list:
        #         print("Name: ", gate.name)
        #         print("Index: ", gate.index)
        #         print("Link ID: ", gate.link_id)
        #         print()

        time_start = time.time()
        for processor in self.physical_processor_list:
            processor.start()

        for processor in self.physical_processor_list:
            processor.join()
        time_end = time.time()

        self.execution_time = time_end - time_start
