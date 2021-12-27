from heqsim.hardware.processor import QuantumProcessor
from heqsim.hardware.state import QuantumState
from heqsim.middleware.link import Link
from heqsim.middleware.bellpairmanager import BellPairManager
import threading
import time
import os


class QuantumCluster:

    def __init__(self):
        self.index_dict = {}
        self.gate_dict = {}
        self.execution_time = 0
        self.network = None

    def prepare_hardware_processor_list(self):
        processor_list = self.network.get_processor_list()
        self.hardware_processor_list = []
        for processor in processor_list:
            processor_info = processor.get_info()
            hardware_processor = QuantumProcessor(processor_info)
            self.hardware_processor_list.append(hardware_processor)

    def prepare_quantum_state(self):
        self.total_qubit_num = 0
        processor_list = self.network.get_processor_list()
        for processor in processor_list:
            self.total_qubit_num += processor.qubit_num
        self.quantum_state = QuantumState(self.total_qubit_num)

    def prepare_link_list(self):
        link_num = self.network.get_link_num()
        self.link_list = [Link() for _ in range(link_num)]

    def get_state(self):
        return self.quantum_state.vector

    def get_execution_time(self):
        return self.execution_time

    def set_index_dict(self, index_dict):
        self.index_dict = index_dict

    def set_gate_dict(self, gate_dict):
        self.gate_dict = gate_dict

    def set_network(self, network):
        self.network = network

    def set_quantum_state_to_processor(self, processor, state):
        processor.state = state

    def set_gate_list_to_processor(self, processor, gate_list):
        processor.gate_list = gate_list

    def set_link_list_to_processor(self, processor, link_list):
        processor.link_list = link_list

    def set_lock_to_processor(self, processor, lock):
        processor.lock = lock

    def set_remote_cnot_manager_to_processor(self, processor, remote_cnot_manager):
        processor.remote_cnot_manager = remote_cnot_manager

    def run(self):

        self.prepare_hardware_processor_list()
        self.prepare_quantum_state()
        self.prepare_link_list()

        lock = threading.Lock()
        remote_cnot_manager = BellPairManager()

        for processor in self.hardware_processor_list:
            self.set_quantum_state_to_processor(processor, self.quantum_state)
            self.set_gate_list_to_processor(processor, self.gate_dict[processor.id])
            self.set_link_list_to_processor(processor, self.link_list)
            self.set_lock_to_processor(processor, lock)
            self.set_remote_cnot_manager_to_processor(processor, remote_cnot_manager)

        time_start = time.time()
        for processor in self.hardware_processor_list:
            processor.start()

        for processor in self.hardware_processor_list:
            processor.join()
        time_end = time.time()

        self.execution_time = time_end - time_start
