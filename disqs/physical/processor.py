from disqs.physical.circuit import PhysicalCircuit
from disqs.device.connection import Connection
import numpy as np
import time
import ray


@ray.remote
class QuantumProcessor(object):
    """A class of a single quantum processor"""

    def __init__(self, detail):
        """Define a quantum processor

        Attributes:
            name (str): the name
            qubit_num (int): the number of qubits
            gates (list[QuantumGate]): the list of quantum gates
            pc (QuantumCircuit): the quantum circuit

        """
        self.id = detail["id"]
        self.qubit_num = detail["qubit_num"]
        self.execution_time = detail["execution_time"]
        self.pc = detail["physical_circuit"]
        self.gates = []

        self.cluster = None
        self.connection_list = []

    def get_id(self):
        """Return the processor id

        Returns:
            str: the name of a quantum processor
        """
        return self.id

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

    def get_state(self):
        """Retreive the current quantum state

        Returns:
            np.array: the state vector
        """
        return self.pc.state

    def set_gates(self, gates):
        """Give the gate list to the quantum processor

        Args:
            gates (list[QuantumGate]): the new list of quantum gates
        """
        self.gates = gates

    def set_cluster(self, cluster):
        """Give the time for applying each gate

        Args:
            cluster (list(QuantumProcessor)): List of quantum processors
        """
        self.cluster = cluster

    def set_connection_list(self, connection_list):
        """Give the time for applying each gate

        Args:
            cluster (list(QuantumProcessor)): List of quantum processors
        """
        self.connection_list = connection_list

    def wait(self):
        time.sleep(self.execution_time)

    def x(self, idx):
        """Apply an X gate

        Args:
            idx (int): The index of qubit that X gate is applied to
        """
        self.pc.px(idx)
        self.wait()

    def y(self, idx):
        """Apply an Y gate

        Args:
            idx (int): The index of qubit that Y gate is applied to
        """
        self.pc.py(idx)
        self.wait()

    def z(self, idx):
        """Apply an Z gate

        Args:
            idx (int): The index of qubit that Z gate is applied to
        """
        self.pc.pz(idx)
        self.wait()

    def h(self, idx):
        """Apply an H gate

        Args:
            idx (int): The index of qubit that H gate is applied to
        """
        self.pc.ph(idx)
        self.wait()

    def cx(self, control_idx, target_idx):
        """Apply an CNOT gate

        Args:
            control_idx (int): The index of controlled qubit
            target_idx (int): The index of target qubit
        """
        self.pc.pcx(control_idx, target_idx)
        self.wait()

    def measure(self, idx):
        measurement_result = self.pc.measure(idx)
        self.wait()
        return measurement_result

    def execute(self):
        """Execute the quantum gates in the given gate list"""
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

            elif gate.name == "RemoteCNOT":
                connection = self.connection_list[gate.id]
                try:
                    connection.send_message(gate.id)
                    ack = connection.get_ack()
                    print(ack)
                except ray.util.queue.Full:
                    message = connection.get_message()
                    connection.send_ack("ack")
                    print(message)

            elif gate.name == "Measure":
                measurement_result = self.measure(gate.index)
