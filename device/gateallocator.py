from logical.gate import QuantumGate


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

        remote_cnot_id = 0  # id for each remote CNOT gate

        for gate in self.gate_list:
            for processor in self.processor_names():

                # single qubit gate
                if gate.target_index is None:
                    if gate.index in index_dict[processor]:
                        self.processor_gate_dict[processor].append(gate)

                # CNOT gates in the same processor
                elif gate.index in index_dict[processor] and gate.target_index in index_dict[processor]:
                    self.processor_gate_dict[processor].append(gate)

                # Remote CNOT gates
                else:
                    # Add remote cnot to the controlled processor
                    if gate.index in index_dict[processor]:

                        [remote_cnot_control, remote_cnot_target] = [QuantumGate("RemoteCNOT", gate.index, gate.target_index) for _ in range(2)]
                        remote_cnot_control.set_id(remote_cnot_id)
                        remote_cnot_target.set_id(remote_cnot_id)

                        remote_cnot_control.set_target_index(None)
                        remote_cnot_control.set_control_processor(processor)

                        for the_other_processor in self.processor_names():

                            # Add remote cnot to the target processor
                            if gate.target_index in index_dict[the_other_processor]:

                                remote_cnot_target.set_index(None)
                                remote_cnot_target.set_target_processor(the_other_processor)
                                self.processor_gate_dict[the_other_processor].append(remote_cnot_target)
                                break

                        self.processor_gate_dict[processor].append(remote_cnot_control)
                        remote_cnot_id += 1

        # Allocate gates to each device
        for processor in self.processors():
            processor_name = self.name(processor)
            processor_indices = index_dict[processor_name]
            gates = self.processor_gate_dict[processor_name]
            for gate in gates:

                # Allocate remote CNOT gates
                if gate.name == "RemoteCNOT":
                    if gate.index is None:
                        gate.target_index = processor_indices.index(gate.target_index)
                    elif gate.target_index is None:
                        gate.index = processor_indices.index(gate.index)

                # Allocate other gates (gates on a local processor)
                else:
                    gate.index = processor_indices.index(gate.index)
                    if gate.target_index is not None:
                        gate.target_index = processor_indices.index(gate.target_index)
            self.set_gates(processor, gates)

        # for processor in list(self.cluster.processor_gate_dict.keys()):
        #     gates = self.cluster.processor_gate_dict[processor]
        #     for gate in gates:
        #         print()
        #         print("Name:", gate.name)
        #         if gate.name == "RemoteCNOT":
        #             print("ID:", gate.id)
        #             if gate.index is not None:
        #                 print("Control index:", gate.index)
        #             if gate.target_index is not None:
        #                 print("Target index:", gate.target_index)
        #             if hasattr(gate, 'control_processor'):
        #                 print("Control processor:", gate.control_processor)
        #             if hasattr(gate, 'target_processor'):
        #                 print("Target processor:", gate.target_processor)
