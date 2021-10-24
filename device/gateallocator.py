
class GateAllocator:
    def __init__(self, gate_list, cluster):
        self.gate_list = gate_list
        self.cluster = cluster
        self.processor_gate_dict = self.processor_gates()

    def processor_gates(self):
        return self.cluster.processor_gate_dict

    def processor_names(self):
        return self.processor_gate_dict.keys()

    def processors(self):
        return self.cluster.processor_list

    def name(self, processor):
        return self.cluster.get_name(processor)

    def gates(self, processor):
        return self.cluster.get_gates(processor)

    def set_gates(self, processor, gates):
        self.cluster.set_gates(processor, gates)

    def execute(self, index_dict):
        for gate in self.gate_list:
            for processor in self.processor_names():
                if gate.index in index_dict[processor]:
                    self.processor_gates()[processor].append(gate)

        for processor in self.processors():
            processor_name = self.name(processor)
            processor_indices = index_dict[processor_name]
            gates = self.processor_gates()[processor_name]
            for gate in gates:
                gate.index = processor_indices.index(gate.index)
                if gate.target_index is not None:
                    gate.target_index = processor_indices.index(
                        gate.target_index)
            self.set_gates(processor, gates)
