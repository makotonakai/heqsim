from physical.processor import QuantumProcessor
from physical.circuit import PhysicalCircuit
import configparser
import ray
import os


class QuantumCluster:

    def __init__(self):
        self.processor_list = []
        self.gate_dict = {}
        self.setup()

    def setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        configdir = '/'.join([path, 'config.ini'])
        config = configparser.ConfigParser()
        config.read(configdir, encoding="utf-8")

        id_ = 0
        for processor_name in config.sections():

            qubit_num = int(config[processor_name]["qubit_num"])
            execution_time = float(config[processor_name]["time"])
            physical_circuit = PhysicalCircuit(qubit_num)

            detail = {"id": id_,
                      "name": processor_name,
                      "qubit_num": qubit_num,
                      "execution_time": execution_time,
                      "physical_circuit": physical_circuit
                      }

            new_processor = QuantumProcessor.remote(detail)
            self.processor_list.append(new_processor)

            self.gate_dict[processor_name] = []
            id_ += 1

        for processor in self.processor_list:
            processor.set_cluster.remote(self.processor_list)

    def new_processor(self):
        return QuantumProcessor.remote()

    def set_cluster(self, processor, cluster):
        processor.set_cluster.remote(cluster)

    def set_gates(self, processor, gates):
        processor.set_gates.remote(gates)

    def get_id(self, processor):
        return ray.get(processor.get_id.remote())

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
