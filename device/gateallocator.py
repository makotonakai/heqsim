from logical.gate import QuantumGate


class GateAllocator:
    def __init__(self, gate_list, cluster):
        self.gate_list = gate_list
        self.cluster = cluster

        self.set_gate_dict()
        self.set_name_list()
        self.set_processor_list()

    def set_gate_dict(self):
        self.gate_dict = self.cluster.gate_dict

    def set_name_list(self):
        self.name_list = list(self.gate_dict.keys())

    def set_processor_list(self):
        self.processor_list = self.cluster.processor_list

    def get_id(self, processor):
        self.self.cluster.get_id(processor)

    def get_name(self, processor):
        return self.cluster.get_name(processor)

    def get_gates(self, processor):
        return self.cluster.get_gates(processor)

    def allocate_gates(self, processor, gates):
        self.cluster.set_gates(processor, gates)

    def execute(self, qubit_dict):

        remote_cnot_id = 0  # id for each remote CNOT gate

        for gate in self.gate_list:

            for processor in self.name_list:

                # single qubit gate
                if gate.target_index is None:
                    if gate.index in qubit_dict[processor]:
                        self.gate_dict[processor].append(gate)

                # CNOT gates in the same processor
                elif gate.index in qubit_dict[processor] and gate.target_index in qubit_dict[processor]:
                    self.gate_dict[processor].append(gate)

                # Remote CNOT gates
                else:
                    # Add remote cnot to the controlled processor
                    if gate.index in qubit_dict[processor]:

                        [remote_cnot_control, remote_cnot_target] = [QuantumGate("RemoteCNOT", gate.index, gate.target_index) for _ in range(2)]

                        remote_cnot_control.set_id(remote_cnot_id)
                        remote_cnot_target.set_id(remote_cnot_id)

                        remote_cnot_control.set_role("control")
                        remote_cnot_target.set_role("target")

                        remote_cnot_control.set_control_processor(processor)
                        remote_cnot_target.set_control_processor(processor)

                        for the_other_processor in self.name_list:

                            # Add remote cnot to the target processor
                            if gate.target_index in qubit_dict[the_other_processor]:

                                remote_cnot_control.set_target_processor(the_other_processor)
                                remote_cnot_target.set_target_processor(the_other_processor)
                                self.gate_dict[the_other_processor].append(remote_cnot_target)
                                break

                        self.gate_dict[processor].append(remote_cnot_control)

                        remote_cnot_id += 1

        # Allocate gates to each device
        for processor in self.processor_list:
            processor_name = self.get_name(processor)
            qubits = qubit_dict[processor_name]
            gates = self.gate_dict[processor_name]

            for gate in gates:

                # Allocate remote CNOT gates
                if gate.name == "RemoteCNOT":
                    control_indices = qubit_dict[gate.control_processor]
                    target_indices = qubit_dict[gate.target_processor]
                    gate.index = control_indices.index(gate.index)
                    gate.target_index = target_indices.index(gate.target_index)

                # Allocate other gates (gates on a local processor)
                else:
                    gate.index = qubits.index(gate.index)
                    if gate.target_index is not None:
                        gate.target_index = qubits.index(gate.target_index)

            self.allocate_gates(processor, gates)

        # for processor in list(self.cluster.gate_dict.keys()):

        #     gates = self.cluster.gate_dict[processor]

        #     for gate in gates:
        #         print()
        #         print("Name:", gate.name)
        #         if gate.name == "CNOT":
        #             print("Control index:", gate.index)
        #             print("Target index:", gate.target_index)
        #         elif gate.name == "RemoteCNOT":
        #             print("ID:", gate.id)
        #             print("Role", gate.role)
        #             print("Control index:", gate.index)
        #             print("Target index:", gate.target_index)
        #             print("Control processor:", gate.control_processor)
        #             print("Target processor:", gate.target_processor)
        #         else:
        #             print("Index:", gate.index)
