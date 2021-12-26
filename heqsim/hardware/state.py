
import numpy as np


class QuantumState:
    """A class for quantum state"""

    def __init__(self, qubit_num):
        """Define a quantum state

        Args:
            qubit_num (int): number of qubits
        """
        self.qubit_num = qubit_num
        self.vector = 1
        self.build_state()

    def build_state(self):
        """Create the initial statevector of the given number of qubits"""
        zero_ket = np.array([1, 0])
        for index in range(self.qubit_num):
            self.vector = np.kron(self.vector, zero_ket)

    def add_state(self, new_state):

        new_qubit_num = new_state.qubit_num
        self.qubit_num += new_qubit_num

        new_vector = new_state.vector
        self.vector = np.kron(self.vector, new_vector)

    def get_statevector(self):
        """return a statevector

        Returns:
            np.array: the statevector
        """
        return self.vector

    def get_qubit_num(self):
        """return the number of qubits

        Returns:
            int: the number of qubits
        """
        return self.qubit_num