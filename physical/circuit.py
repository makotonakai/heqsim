
from .gate import px_, py_, pz_, ph_, pcx_
from .state import PhysicalState
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

    def px(self, idx):
        """Applying an X gate

        Args:
            idx (int): the index of a qubit that users are going to apply this gate
        """
        xmatrix = px_(self.qubit_num, idx)
        self.state = np.dot(xmatrix, self.state)

    def py(self, idx):
        """Applying an Y gate

        Args:
            idx (int): the index of a qubit that users are going to apply this gate
        """
        ymatrix = py_(self.qubit_num, idx)
        self.state = np.dot(ymatrix, self.state)

    def pz(self, idx):
        """Applying an Z gate

        Args:
            idx (int): the index of a qubit that users are going to apply this gate
        """
        zmatrix = pz_(self.qubit_num, idx)
        self.state = np.dot(zmatrix, self.state)

    def ph(self, idx):
        """Applying an H gate

        Args:
            idx (int): the index of a qubit that users are going to apply this gate
        """
        hmatrix = ph_(self.qubit_num, idx)
        self.state = np.dot(hmatrix, self.state)

    def pcx(self, control_idx, target_idx):
        """Applying a CNOT gate

        Args:
            idx (int): the index of a qubit that users are going to apply this gate
        """
        cxmatrix = pcx_(self.qubit_num, control_idx, target_idx)
        self.state = np.dot(cxmatrix, self.state)

    def measure(self, idx):
        """Measure a qubit

        Args:
            idx (int): the index of a qubit that users measure
        """
        prob = [prob_amp**2 for prob_amp in self.state]

        prob_dict = {}
        for state in range(len(prob)):
            prob_dict[format(state, 'b').zfill(self.qubit_num)] = prob[state]

        measure_prob = [0, 0]
        for state in list(prob_dict.keys()):
            if state[idx] == "0" and prob_dict[state] > 0:
                measure_prob[0] += 1
            elif state[idx] == "1" and prob_dict[state] > 0:
                measure_prob[1] += 1
        measure_prob = [num / sum(measure_prob) for num in measure_prob]
        measure_result = np.random.choice(range(2), 1, p=measure_prob)[0]

        # 状態ベクトルを更新
        state_dict = {}
        for state in range(len(prob)):
            index = format(state, 'b').zfill(self.qubit_num)
            state_dict[index] = self.state[state]

        new_state_dict = {}
        for state in list(state_dict.keys()):
            if state[idx] == str(measure_result):
                state_list = list(state)
                del state_list[idx]
                new_state = "".join(state_list)

                if 1 in state_dict.values():
                    new_state_dict[new_state] = state_dict[state]
                else:
                    new_state_dict[new_state] = state_dict[state] * np.sqrt(2)

        return measure_result
