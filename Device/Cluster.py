from .Processor import QuantumProcessor
import configparser
import sys
import os

class QuantumCluster:

    def __init__(self):
        self.processor_list = []
        self.qubit_number = 0
        self.index_dict = {processor.device_name:[] for processor in self.processor_list}
        self.gate_dict = {processor.device_name:[] for processor in self.processor_list}
        self.cxgraph = {str(idx):[] for idx in range(self.qubit_number)}
        self.setup()
        self.sort_processor()

    def setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        configdir = '/'.join([path,'config.ini'])
        config = configparser.ConfigParser()
        config.read(configdir, encoding="utf-8")

        for device_name in config.sections():
            qubit_number = int(config[device_name]["qubit_number"])
            single_qubit_gate_time = float(config[device_name]["single_qubit_gate_time"])
            two_qubit_gate_time = float(config[device_name]["two_qubit_gate_time"])
            new_processor = QuantumProcessor(device_name, qubit_number, single_qubit_gate_time, two_qubit_gate_time)
            self.processor_list.append(new_processor) 

        for processor in self.processor_list:
            self.qubit_number += processor.qubit_number

    def sort_processor(self):
        self.processor_list.sort(key=lambda processor:processor.single_qubit_gate_time)
        

    def remote_cnot(self, first_processor_index, second_processor_index, first_qubit_index, second_qubit_index):
        first_processor = self.processor_list[first_processor_index]
        second_processor = self.processor_list[second_processor_index]


    def add_qubit(self, index):
        processor = self.processor_list[0]
        processor.add_qubit(index)
        qc = processor.pc
        return qc.state