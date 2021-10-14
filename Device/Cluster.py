from .processor import QuantumProcessor
from logical.gate import QuantumGate
import configparser
import ray
import sys
import os

class QuantumCluster:

    def __init__(self):
        self.qubit_number = 0
        self.processor_list = []
        self.setup()
        
        self.index_dict = {processor.device_name:[] for processor in self.processor_list}
        self.gate_dict = {processor.device_name:[] for processor in self.processor_list}
        self.state_list = []

    def setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        configdir = '/'.join([path,'config.ini'])
        config = configparser.ConfigParser()
        config.read(configdir, encoding="utf-8")

        for device_name in config.sections():
            new_processor = QuantumProcessor.remote()
            qubit_number = int(config[device_name]["qubit_number"])
            single_qubit_gate_time = float(config[device_name]["single_qubit_gate_time"])
            two_qubit_gate_time = float(config[device_name]["two_qubit_gate_time"])

            new_processor.set_device_name(device_name).remote()
            new_processor.set_qubit_number(qubit_number).remote()
            new_processor.set_single_qubit_gate_time(single_qubit_gate_time).remote()
            new_processor.set_two_qubit_gate_time(two_qubit_gate_time).remote()
            
            self.processor_list.append(new_processor) 

        for processor in self.processor_list:

            self.qubit_number += processor.qubit_number

        self.processor_list.sort(key=lambda processor:processor.single_qubit_gate_time)

    def run_circuit(self):

        for processor in self.processor_list:
            gate_list = self.gate_dict[processor.name]
            for gate in gate_list:
                if gate.name == "X":
                    processor.pc.x(gate.index).remote()
                elif gate.name == "Y":
                    processor.pc.y(gate.index).remote()
                elif gate.name == "Z":
                    processor.pc.z(gate.index).remote()
                elif gate.name == "H":
                    processor.pc.h(gate.index).remote()
                elif gate.name == "CNOT":
                    processor.pc.cx(gate.index, gate.target_index).remote()
            state = ray.get(processor.pc.state)
            self.state_list.append(state)
        
        for state in self.state_list:
            print(state)


    def remote_cnot(self, first_processor_index, second_processor_index, first_qubit_index, second_qubit_index):
        first_processor = self.processor_list[first_processor_index]
        second_processor = self.processor_list[second_processor_index]


    def add_qubit(self, index):
        processor = self.processor_list[0]
        processor.add_qubit(index)
        qc = processor.pc
        return qc.state