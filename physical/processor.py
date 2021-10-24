from physical.circuit import PhysicalCircuit
import ray


@ray.remote
class QuantumProcessor(object):

    def __init__(self):
        self.name = None
        self.qubit_num = 0
        self.gates = []
        self.pc = None

    def get_name(self):
        return self.name

    def get_gates(self):
        return self.gates

    def get_qubit_num(self):
        return self.qubit_num

    def set_name(self, new_name):
        self.name = new_name

    def set_qubit_num(self, qubit_num):
        self.qubit_num = qubit_num

    def set_quantum_circuit(self):
        self.pc = PhysicalCircuit(self.qubit_num)

    def set_gates(self, gates):
        self.gates = gates

    def x(self, idx):
        self.pc.px(idx)

    def y(self, idx):
        self.pc.py(idx)

    def z(self, idx):
        self.pc.pz(idx)

    def h(self, idx):
        self.pc.ph(idx)

    def cx(self, control_idx, target_idx):
        self.pc.pcx(control_idx, target_idx)

    def execute(self):
        for gate in self.gates:
            if gate.name == "X":
                self.x(gate.index)
            elif gate.name == "Y":
                self.y(gate.index)
            elif gate.name == "Z":
                self.z(gate.index)
            elif gate.name == "H":
                self.h(gate.index)
            elif gate.name == "CNOT":
                self.cx(gate.index, gate.target_index)

    def get_state(self):
        return self.pc.state

    def add_new_zero(self, num, new_index):
        string = bin(num)[2:].zfill(self.qubit_num)
        string_list = list(string)
        string_list.insert(new_index, '0')
        new_string = "".join(string_list)
        return new_string

    def add_qubit(self, new_index):
        state_dict = {}
        for idx in range(len(self.pc.state)):
            new_idx = self.add_new_zero(idx, new_index)
            state_dict[new_idx] = self.pc.state[idx]

        new_state = [0 for idx in range(2**(self.qubit_num + 1))]
        for key in list(state_dict.keys()):
            new_idx = int(key, 2)
            new_state[new_idx] = state_dict[key]
        self.pc.state = new_state
