from physical.processor import QuantumProcessor
from logical.gate import QuantumGate
import configparser
import ray
import sys
import os

class QuantumCluster:

    def __init__(self):
        self.total_qubit_num = 0
        self.processor_dict = {}
        self.state_list = []
        self.setup()

    def setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        configdir = '/'.join([path,'config.ini'])
        config = configparser.ConfigParser()
        config.read(configdir, encoding="utf-8")

        for device_name in config.sections():
            qubit_num = int(config[device_name]["qubit_num"])
            self.processor_dict[device_name] = qubit_num

            new_processor = QuantumProcessor.remote()
            new_processor.set_device_name.remote(device_name)
            new_processor.set_qubit_num(qubit_num)
            new_processor.set_quantum_circuit.remote()

    

    def remote_cnot(self, first_processor_index, second_processor_index, first_qubit_index, second_qubit_index):
        first_processor = self.processor_list[first_processor_index]
        second_processor = self.processor_list[second_processor_index]


    