from disqs.physical.processor import PhysicalProcessor
from disqs.physical.state import QuantumState
from disqs.device.connection import Connection
import threading
import configparser
import time
import os


class QuantumCluster:

    def __init__(self):
        self.processor_list = []
        self.index_dict = {}
        self.gate_dict = {}
        self.remote_cnot_num = 0

        self.total_qubit_num = 0
        self.setup()

    def setup(self):

        path = os.path.dirname(os.path.realpath(__file__))
        configdir = '/'.join([path, 'config.ini'])
        config = configparser.ConfigParser()
        config.read(configdir, encoding="utf-8")

        sections = config.sections()
        id_ = 0

        for processor_ in sections:

            qubit_num = int(config[processor_]["qubit_num"])
            execution_time = float(config[processor_]["time"])

            detail = {
                "id": id_,
                "qubit_num": qubit_num,
                "execution_time": execution_time}

            processor = PhysicalProcessor(detail)
            self.processor_list.append(processor)

            self.total_qubit_num += qubit_num

            self.gate_dict[id_] = []
            id_ += 1

        self.set_quantum_state()

    def get_id(self, processor):
        return processor.id

    def get_qubit_num(self, processor):
        return processor.qubit_num

    def set_quantum_state(self):
        self.state = QuantumState(self.total_qubit_num)

    def set_index_dict(self, index_dict):
        self.index_dict = index_dict

    def set_connection_list(self, connection_list):
        self.connection_list = connection_list

    def set_remote_cnot_num(self, remote_cnot_num):
        self.remote_cnot_num = remote_cnot_num

    def set_index_list_to_processor(self, processor, index_list):
        processor.index_list = index_list

    def set_gate_list_to_processor(self, processor, gate_list):
        processor.gate_list = gate_list

    def set_quantum_state_to_processor(self, processor, state):
        processor.state = state

    def set_lock_to_processor(self, processor, lock):
        processor.lock = lock

    def set_connection_list_to_processor(self, processor, connection_list):
        processor.connection_list = connection_list

    def run(self):

        lock = threading.Lock()
        connection_list = [Connection() for _ in range(self.remote_cnot_num)]

        for processor in self.processor_list:
            self.set_gate_list_to_processor(processor, self.gate_dict[processor.id])
            self.set_quantum_state_to_processor(processor, self.state)
            self.set_lock_to_processor(processor, lock)
            self.set_connection_list_to_processor(processor, connection_list)

        for processor in self.processor_list:
            processor.start()

        for processor in self.processor_list:
            processor.join()
