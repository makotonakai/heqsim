from physical.processor import QuantumProcessor
from logical.gate import QuantumGate
import configparser
import ray
import sys
import os

class QuantumCluster:

    def __init__(self):
        self.total_qubit_num = 0
        self.processor_list = []
        self.processor_index_dict = {}
        self.processor_gate_dict = {}
        self.setup()

    def setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        configdir = '/'.join([path,'config.ini'])
        config = configparser.ConfigParser()
        config.read(configdir, encoding="utf-8")

        for processor_name in config.sections():

            qubit_num = int(config[processor_name]["qubit_num"])
            self.processor_index_dict[processor_name] = qubit_num
            self.total_qubit_num += qubit_num

            self.processor_gate_dict[processor_name] = []

            new_processor = self.new_processor()
            self.set_name(new_processor, processor_name)
            self.set_qubit_num(new_processor, qubit_num)
            self.set_quantum_circuit(new_processor)
            self.processor_list.append(new_processor)
            
    def new_processor(self):
        return QuantumProcessor.remote()

    def set_name(self, processor, new_name):
        processor.set_name.remote(new_name)

    def set_qubit_num(self, processor, new_qubit_num):
        processor.set_qubit_num.remote(new_qubit_num)

    def set_quantum_circuit(self, processor):
        processor.set_quantum_circuit.remote()

    def set_gates(self, processor, gates):
        processor.set_gates.remote(gates)

    def get_name(self, processor):
        return ray.get(processor.get_name.remote())

    def get_qubit_num(self, processor):
        return ray.get(processor.get_qubit_num.remote())

    def get_gates(self, processor):
        return ray.get(processor.get_gates.remote())

    def get_state(self, processor):
        return ray.get(processor.get_state.remote())

    def execute_on_each_processor(self, processor):
        processor.execute.remote()

    def execute(self):
        for processor in self.processor_list:
            self.execute_on_each_processor(processor)



    

    

    