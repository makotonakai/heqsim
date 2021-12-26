
from heqsim.physical.gate import px_, py_, pz_, ph_, pcx_
from heqsim.physical.state import PhysicalState
import numpy as np


class PhysicalCircuit:
    """A class for quantum circuit"""

    def __init__(self, n):
        """Create a quantum circuit on a physical processor

        Args:
            n (int): number of qubits on a quantum circuit
        """
        self.qubit_num = n
        self.state = PhysicalState(self.qubit_num).get_statevector()

    def px(self, index):
        """Applying an X gate

        Args:
            index (int): the index of a qubit that users are going to apply this gate
        """
        xmatrix = px_(self.qubit_num, index)
        self.state = np.dot(xmatrix, self.state)

    def py(self, index):
        """Applying an Y gate

        Args:
            index (int): the index of a qubit that users are going to apply this gate
        """
        ymatrix = py_(self.qubit_num, index)
        self.state = np.dot(ymatrix, self.state)

    def pz(self, index):
        """Applying an Z gate

        Args:
            index (int): the index of a qubit that users are going to apply this gate
        """
        zmatrix = pz_(self.qubit_num, index)
        self.state = np.dot(zmatrix, self.state)

    def ph(self, index):
        """Applying an H gate

        Args:
            index (int): the index of a qubit that users are going to apply this gate
        """
        hmatrix = ph_(self.qubit_num, index)
        self.state = np.dot(hmatrix, self.state)

    def pcx(self, control_index, target_index):
        """Applying a CNOT gate

        Args:
            index (int): the index of a qubit that users are going to apply this gate
        """
        cxmatrix = pcx_(self.qubit_num, control_index, target_index)
        self.state = np.dot(cxmatrix, self.state)

    def measure(self, index):
        """Measure a qubit

        Args:
            index (int): the index of a qubit that users measure
        """

        # Measurement probability of the measured qubit
        measure_prob = {"0": 0, "1": 0}

        # Pairs of state & its probability amplitude
        state_dict = {}
        qubit_num = int(np.log2(len(self.state)))
        for num in range(len(self.state)):
            comp_basis = bin(num)[2:].zfill(qubit_num)
            state_dict[comp_basis] = self.state[num]

        # Calculate measurement probability of the measured qubit
        for key in list(state_dict.keys()):
            if key[index] == "0":
                measure_prob["0"] += state_dict[key]**2
            else:
                measure_prob["1"] += state_dict[key]**2

        # Perform measurement
        measure_result = np.random.choice(2, 1, p=list(measure_prob.values()))[0]

        # Pairs of each of the updated states & its probability amplitude
        new_state_dict = {}
        for num in range(len(self.state)):
            comp_basis = bin(num)[2:].zfill(qubit_num)
            if comp_basis[index] == str(measure_result):
                comp_basis_list = list(comp_basis)
                del comp_basis_list[index]
                new_comp_basis = "".join(comp_basis_list)
                new_state_dict[new_comp_basis] = self.state[num]

        # Update each of the probability amplitudes
        for key in list(new_state_dict.keys()):
            prob_list = [new_state_dict[key]**2 for key in list(new_state_dict.keys())]
            new_state_dict[key] *= np.sqrt(1 / sum(prob_list))

        self.state = np.array(list(new_state_dict.values()))
        return measure_result
