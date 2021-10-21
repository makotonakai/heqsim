from .gate import QuantumGate
from device.cluster import QuantumCluster
from device.indexallocator import IndexAllocator
from device.gateallocator import GateAllocator
import numpy as np

class QuantumCircuit:

    def __init__(self, qubit_num):
        self.qubit_num = qubit_num
        self.gate_list = []

        self.cluster = QuantumCluster()
        self.index_allocator = IndexAllocator(self.qubit_num, self.cluster)
        self.gate_allocator = GateAllocator(self.gate_list, self.cluster)

    def x(self, idx):
        self.gate_list.append(QuantumGate("X", idx))

    def y(self, idx):
        self.gate_list.append(QuantumGate("Y", idx))
        
    def z(self, idx):
        self.gate_list.append(QuantumGate("Z", idx))

    def h(self, idx):
        self.gate_list.append(QuantumGate("H", idx))

    def cx(self, control_idx, target_idx):
        self.gate_list.append(QuantumGate("CX", control_idx, target_idx))

    def allocate_indices(self):
        self.index_allocator.execute()

    def get_indices(self):
        index_dict = self.index_allocator.get_result()
        return index_dict

    def allocate_gates(self):
        index_dict = self.get_indices()
        self.gate_allocator.execute(index_dict)

    def run_cluster(self):
        self.cluster.execute()

    def execute(self):
        self.allocate_indices()
        self.allocate_gates()
        self.run_cluster()

    def name(self, processor):
        return self.cluster.get_name(processor)

    def state(self, processor):
        return self.cluster.get_state(processor)

    def qubits(self, processor):
        return self.cluster.get_qubit_num(processor)

    def processor_list(self):
        return self.cluster.processor_list

    def state_str(self, num, digit):
        return bin(num)[2:].zfill(digit)

    def is_part_of_state(self, indices, state_str, target_state_str):
        total_state_str_shrinked = "".join([target_state_str[index] for index in indices])
        return state_str == total_state_str_shrinked

    def result(self):
        total_state_dir = {self.state_str(state, self.qubit_num):1 for state in range(2**self.qubit_num)}
        
        for processor in self.processor_list():
            qubit_num = self.qubits(processor)
            state = self.state(processor)
            state_dir = {self.state_str(qubit_idx, qubit_num):state[qubit_idx] for qubit_idx in range(2**qubit_num)}

            processor_name = self.name(processor)
            indices = self.get_indices()[processor_name]

            total_states = list(total_state_dir.keys())
            states = list(state_dir.keys())
            
            for total_state in total_states:
                for each_state in states:
                    if self.is_part_of_state(indices, each_state, total_state) == True:
                        total_state_dir[total_state] *= state_dir[each_state]

        total_state = np.array(list(total_state_dir.values()))
        return total_state
        



    
    



    
    

        

