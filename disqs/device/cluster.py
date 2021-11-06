from disqs.physical.processor import QuantumProcessor
from disqs.physical.circuit import PhysicalCircuit
from disqs.device.connection import Connection
import configparser
import time
import ray
import os


class QuantumCluster:

    def __init__(self):
        self.processor_list = []
        self.gate_dict = {}
        self.remote_cnot_list = []
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
            physical_circuit = PhysicalCircuit(qubit_num)

            detail = {"id": id_,
                      "qubit_num": qubit_num,
                      "execution_time": execution_time,
                      "physical_circuit": physical_circuit
                      }

            processor = QuantumProcessor.remote(detail)
            self.processor_list.append(processor)

            self.gate_dict[id_] = []
            id_ += 1

        for processor in self.processor_list:
            processor.set_cluster.remote(self.processor_list)

    def set_cluster(self, processor, cluster):
        processor.set_cluster.remote(cluster)

    def set_gates(self, processor, gates):
        processor.set_gates.remote(gates)

    def set_connection_list(self, processor):
        processor.set_connection_list.remote(self.connection_list)

    def create_connection_list(self):
        self.connection_list = []
        for remote_cnot_id in range(len(self.remote_cnot_list)):
            if remote_cnot_id % 2 == 0:
                connection = Connection()
                self.connection_list.append(connection)

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

    def execute(self):
        self.create_connection_list()
        for processor in self.processor_list:
            self.set_connection_list(processor)

        result = ray.get([processor.execute.remote() for processor in self.processor_list])
        # self.state_list = ray.get([processor.get_state.remote() for processor in self.processor_list])
