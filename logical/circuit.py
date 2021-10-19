from .gate import QuantumGate
from device.cluster import QuantumCluster
from device.indexallocator import IndexAllocator
from device.gateallocator import GateAllocator

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
        index_dict = self.index_allocator.get_result()
        return index_dict

    def allocate_gates(self):
        index_dict = self.allocate_indices()
        self.gate_allocator.execute(index_dict)

    def run_cluster(self):
        self.cluster.execute()

    def execute(self):
        self.allocate_gates()
        self.run_cluster()

    def state(self, processor):
        return self.cluster.get_state(processor)

    def processor_list(self):
        return self.cluster.processor_list

    def result(self):
        state_list = []
        for processor in self.processor_list():
            each_state = self.state(processor)
            state_list.append(each_state)
        return state_list

    
    



    
    

        

