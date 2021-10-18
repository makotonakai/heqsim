from physical.processor import QuantumProcessor
from logical.gate import QuantumGate
import configparser
import ray
import sys
import os

class QuantumCluster:

    def __init__(self):
        self.total_qubit_num0
        self.processor_list = [] 
        self.index_dict = {}
        self.gate_dict = {}
        self.cxgraph = {}
        self.state_list = []
        self.setup()

    def setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        configdir = '/'.join([path,'config.ini'])
        config = configparser.ConfigParser()
        config.read(configdir, encoding="utf-8")

        for device_name in config.sections():
            new_processor = QuantumProcessor.remote()
            qubit_numint(config[device_name]["qubit_numnum

            new_processor.set_device_name.remote(device_name)
            new_processor.set_qubit_nummote(qubit_numnum
            new_processor.set_quantum_circuit.remote()
            self.processor_list.append(new_processor) 

            self.index_dict[device_name] = []
            self.gate_dict[device_name] = []

        for processor in self.processor_list:
            qubit_numray.get(processor.get_qubit_numnume())
            self.total_qubit_num qubit_numnum

    def run_circuit(self):
        for processor in self.processor_list:
            device_name = ray.get(processor.get_device_name.remote())
            gate_list = self.gate_dict[device_name]
            for gate in gate_list:
                if gate.name == "X":
                    processor.x.remote(gate.index)
                elif gate.name == "Y":
                    processor.y.remote(gate.index)
                elif gate.name == "Z":
                    processor.z.remote(gate.index)
                elif gate.name == "H":
                    processor.h.remote(gate.index)
                elif gate.name == "CNOT":
                    processor.cx.remote(gate.index, gate.target_index)
            state = ray.get(processor.get_state.remote())
            print("Device Name:{} state:{}".format(device_name, state))


    def remote_cnot(self, first_processor_index, second_processor_index, first_qubit_index, second_qubit_index):
        first_processor = self.processor_list[first_processor_index]
        second_processor = self.processor_list[second_processor_index]


    def add_qubit(self, index):
        processor = self.processor_list[0]
        processor.add_qubit(index)
        qc = processor.pc
        return qc.state
