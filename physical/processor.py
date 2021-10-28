from physical.circuit import PhysicalCircuit
import numpy as np
import time
import ray


@ray.remote
class QuantumProcessor(object):
    """A class of a single quantum processor"""

    def __init__(self):
        """Define a quantum processor

        Attributes:
            name (str): the name
            qubit_num (int): the number of qubits
            gates (list[QuantumGate]): the list of quantum gates
            pc (QuantumCircuit): the quantum circuit

        """
        self.name = None
        self.qubit_num = 0
        self.time = 0
        self.gates = []
        self.pc = None

    def get_name(self):
        """Return the processor name

        Returns:
            str: the name of a quantum processor
        """
        return self.name

    def get_gates(self):
        """Return the quantum gate list

        Returns:
            list[QuantumGate]: List of quantum gates
        """
        return self.gates

    def get_qubit_num(self):
        """Return the number of qubits

        Returns:
            int: the number of qubits on a quantum processor
        """
        return self.qubit_num

    def set_name(self, new_name):
        """Give a new name to the quantum processor

        Args:
            new_name (str): the new name in a quantum processor
        """
        self.name = new_name

    def set_qubit_num(self, qubit_num):
        """Give the number of qubits to the quantum processor

        Args:
            qubit_num (int): the number of qubits
        """
        self.qubit_num = qubit_num

    def set_time(self, time):
        """Give the time for applying each gate

        Args:
            time (float): How long it takes to apply single gate
        """
        self.time = time

    def set_quantum_circuit(self):
        """Give the quantum circuit to the quantum processor"""
        self.pc = PhysicalCircuit(self.qubit_num)

    def set_gates(self, gates):
        """Give the gate list to the quantum processor

        Args:
            gates (list[QuantumGate]): the new list of quantum gates
        """
        self.gates = gates

    def x(self, idx):
        """Apply an X gate

        Args:
            idx (int): The index of qubit that X gate is applied to
        """
        self.pc.px(idx)

    def y(self, idx):
        """Apply an Y gate

        Args:
            idx (int): The index of qubit that Y gate is applied to
        """
        self.pc.py(idx)

    def z(self, idx):
        """Apply an Z gate

        Args:
            idx (int): The index of qubit that Z gate is applied to
        """
        self.pc.pz(idx)

    def h(self, idx):
        """Apply an H gate

        Args:
            idx (int): The index of qubit that H gate is applied to
        """
        self.pc.ph(idx)

    def cx(self, control_idx, target_idx):
        """Apply an CNOT gate

        Args:
            control_idx (int): The index of controlled qubit
            target_idx (int): The index of target qubit
        """
        self.pc.pcx(control_idx, target_idx)

    def execute(self):
        """Execute the quantum gates in the given gate list"""
        for gate in self.gates:
            if gate.name == "X":
                self.x(gate.index)
                time.sleep(self.time)

            elif gate.name == "Y":
                self.y(gate.index)
                time.sleep(self.time)

            elif gate.name == "Z":
                self.z(gate.index)
                time.sleep(self.time)
            elif gate.name == "H":
                self.h(gate.index)
                time.sleep(self.time)

            elif gate.name == "CNOT":
                self.cx(gate.index, gate.target_index)
                time.sleep(self.time)

            elif gate.name == "RemoteCNOT":
                print("{} got remote CNOT".format(self.name))

    def get_state(self):
        """Retreive the current quantum state

        Returns:
            np.array: the state vector
        """
        return self.pc.state

    def add_new_zero(self, num, new_index):
        """Insert zero to arbitrary position of a binary string

        E.g. insert 0 to the 2nd digit of 010 → 0010

        Args:
            num (int): the number
            new_index ([type]): the index of a new zero

        Returns:
            str: the binary string with an additional zero
        """
        string = bin(num)[2:].zfill(self.qubit_num)
        string_list = list(string)
        string_list.insert(new_index, '0')
        new_string = "".join(string_list)
        return new_string

    def add_qubit(self, new_index):
        """Update the quantum state by adding another qubit

        Args:
            new_index (int): the index of the new qubit
        """
        state_dict = {}
        for idx in range(len(self.pc.state)):
            new_idx = self.add_new_zero(idx, new_index)
            state_dict[new_idx] = self.pc.state[idx]

        new_state = [0 for idx in range(2**(self.qubit_num + 1))]
        for key in list(state_dict.keys()):
            new_idx = int(key, 2)
            new_state[new_idx] = state_dict[key]
        self.pc.state = new_state

    def measure(self, idx):
        """Measure a qubit
        Args:
            idx (int): the index of a qubit that users measure
        """
        # Create a probability list
        prob = [prob_amp**2 for prob_amp in self.state]
        prob_dict = {}
        for state_ in range(len(prob)):
            prob_dict[format(state_, 'b').zfill(self.qubit_num)] = prob[state_]

        # Get a measured outcome
        measure_prob = [0, 0]
        for state_ in list(prob_dict.keys()):
            if state_[idx] == "0":
                measure_prob[0] += prob_dict[state_]
            else:
                measure_prob[1] += prob_dict[state_]
        measure_result = np.random.choice(range(2), 1, p=measure_prob)[0]

        # Update a previous state dict (state: probability amplitude)
        state_dict = {}
        for state_ in range(len(prob)):
            index = format(state_, 'b').zfill(self.ubit_num)
            state_dict[index] = self.state[state_]

        new_state_dict = {}
        for state_ in list(state_dict.keys()):
            if state_[idx] == str(measure_result):
                state_list = list(state_)
                del state_list[idx]
                new_state = "".join(state_list)
                new_state_dict[new_state] = state_dict[state_]

        new_prob = [prob_amp**2 for prob_amp in list(new_state_dict.values())]
        for state_ in list(new_state_dict.keys()):
            new_state_dict[state_] *= np.sqrt(1 / sum(new_prob))

        new_state = np.array(list(new_state_dict.values()))
        self.state = new_state
        return measure_result
