from disqs.logical.gate import QuantumGate


class GateAllocator:
    def __init__(self, gate_list, cluster):
        self.gate_list = gate_list
        self.cluster = cluster

    def set_gate_dict_to_cluster(self, gate_dict):
        self.cluster.set_gate_dict(gate_dict)

    def execute(self, qubit_dict, network):

        self.processor_list = network.get_processor_list()
        self.gate_dict = {processor.id: [] for processor in self.processor_list}

        remote_cnot_id = 0  # id for each remote CNOT gate

        for gate in self.gate_list:

            for processor in self.processor_list:

                processor_id = processor.id

                # single qubit gate
                if gate.target_index is None:
                    if gate.index in qubit_dict[processor_id]:
                        self.gate_dict[processor_id].append(gate)

                # CNOT gates in the same processor
                elif gate.index in qubit_dict[processor_id] and gate.target_index in qubit_dict[processor_id]:
                    self.gate_dict[processor_id].append(gate)

                # Remote CNOT gates
                else:
                    # Add remote cnot to the controlled processor
                    if gate.index in qubit_dict[processor_id]:

                        [remote_cnot_control, remote_cnot_target] = [QuantumGate("RemoteCNOT", gate.index, gate.target_index) for _ in range(2)]

                        remote_cnot_control.set_id(remote_cnot_id)
                        remote_cnot_target.set_id(remote_cnot_id)

                        remote_cnot_control.set_role("control")
                        remote_cnot_target.set_role("target")

                        control_id = processor_id
                        remote_cnot_control.set_control_id(control_id)
                        remote_cnot_target.set_control_id(control_id)

                        for the_other_processor in self.processor_list:

                            # Add remote cnot to the target processor
                            target_id = the_other_processor.id
                            if gate.target_index in qubit_dict[target_id]:
                                remote_cnot_control.set_target_id(target_id)
                                remote_cnot_target.set_target_id(target_id)
                                self.gate_dict[target_id].append(remote_cnot_target)
                                break

                        self.gate_dict[control_id].append(remote_cnot_control)
                        remote_cnot_id += 1

        self.set_gate_dict_to_cluster(self.gate_dict)
