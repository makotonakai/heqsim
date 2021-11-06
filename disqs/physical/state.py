
import numpy as np


class PhysicalState:
    """A class for quantum state"""

    def __init__(self, qubit_num):
        """Define a quantum state

        Args:
            qubit_num (int): number of qubits
        """
        self.qubit_num = qubit_num
        self.statevector = 1
        self.build_state()

    def build_state(self):
        """Create the initial statevector of the given number of qubits"""
        state_qubit = np.array([1, 0])
        for index in range(self.qubit_num):
            self.statevector = np.kron(self.statevector, state_qubit)

    def get_statevector(self):
        """return a statevector

        Returns:
            np.array: the statevector
        """
        return self.statevector
