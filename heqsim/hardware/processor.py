from heqsim.hardware.state import QuantumState
from heqsim.hardware.gate import x, y, z, h, cnot, measure, rx, ry, rz, phase, swap
from heqsim.middleware.link import Link
from threading import Thread
import numpy as np
import queue
import time


class QuantumProcessor(Thread):
    """A class which emulates a physical quantum processor

    Args:
        Thread (threading.Thread): A thread used for parallel execution of a quantum circuit
    """

    def __init__(self, param):
        """Create a quantum processor

        Args:
            param (dict): A directory which contains
                            {
                                "id": processor id,
                                "qubit_num": number of qubits in a quantum processor,
                                "execution time": execution time of a single quantum gate in a quantum processor
                            }
        """
        Thread.__init__(self)
        self.id = param["id"]
        self.qubit_num = param["qubit_num"] + 2
        self.execution_time = param["execution_time"]

        self.state = None
        self.gate_list = None

        self.link_list = None
        self.comm_qubit_manager = None
        self.bell_pair_manager = None
        self.lock = None

    def run(self):
        """ the method to run the quantum circuit """

        for gate in self.gate_list:

            # X gate
            if gate.name == "X":
                x(self.state, gate.index, self.execution_time, self.lock)

            # Y gate
            elif gate.name == "Y":
                y(self.state, gate.index, self.execution_time, self.lock)

            # Z gate
            elif gate.name == "Z":
                z(self.state, gate.index, self.execution_time, self.lock)

            # H gate
            elif gate.name == "H":
                h(self.state, gate.index, self.execution_time, self.lock)

            # Local CNOT gate
            elif gate.name == "CNOT":
                cnot(self.state, gate.index, gate.target_index, self.execution_time, self.lock)

            # Rx gate
            elif gate.name == "RX":
                rx(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            # Ry gate
            elif gate.name == "RY":
                ry(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            # Rz gate
            elif gate.name == "RZ":
                rz(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            # Phase gate
            elif gate.name == "PHASE":
                phase(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            # SWAP gate
            elif gate.name == "SWAP":
                swap(self.state, gate.index, gate.target_index, self.execution_time, self.lock)

            # Create an entanglement between two quantum processors
            elif gate.name == "ENTANGLE":

                self.lock.acquire()

                link = self.link_list[gate.link_id]

                if link.classical_link.empty():

                    conn_manager = self.connection_manager
                    conn_dict = conn_manager.get_dict()
                    link.send_classical_message("entangle")

                    if gate.role == "control":
                        control_index = conn_dict[self.id][1]
                        target_index = conn_dict[self.id + 1][0]
                        h(self.state, control_index, self.execution_time, None)
                        cnot(self.state, control_index, target_index, self.execution_time, None)

                    else:
                        control_index = conn_dict[self.id][0]
                        target_index = conn_dict[self.id - 1][1]
                        h(self.state, control_index, self.execution_time, None)
                        cnot(self.state, control_index, target_index, self.execution_time, None)

                else:
                    message = link.get_classical_message()

                self.lock.release()

            # Perform bell measurement
            elif gate.name == "BELL_MEASUREMENT":
                pass

            # Send a measurement result
            elif gate.name == "SEND":
                self.lock.acquire()
                link = self.link_list[gate.link_id]
                if gate.role == "control":
                    link.send_control_message(self.measurement_result)
                else:
                    link.send_target_message(self.measurement_result)
                self.lock.release()

            # Receive a measurement result
            elif gate.name == "GET":

                link = self.link_list[gate.link_id]
                if gate.role == "control":
                    measurement_result = link.get_control_message()
                else:
                    measurement_result = link.get_target_message()
                self.measurement_result = measurement_result

            # Apply operations before sending the measurement result on the control processor
            elif gate.name == "FORWARD_CONTROL":

                self.lock.acquire()

                conn_manager = self.connection_manager
                conn_dict = conn_manager.get_dict()

                target_index = conn_dict[self.id][1]
                cnot(self.state, gate.index, target_index, self.execution_time, None)

                measurement_result = measure(self.state, target_index, self.execution_time, None)
                self.measurement_result = measurement_result

                qubit = QuantumState(1)
                self.state.add_state(qubit)

                self.connection_manager.remove_qubit(self.id, 1)
                self.connection_manager.add_qubit(self.id, 1)

                link = self.link_list[gate.link_id]
                link.send_control_message(self.measurement_result)

                self.lock.release()

            # Apply operations after receiving the measurement result from the control processor
            elif gate.name == "FORWARD_TARGET":

                self.lock.acquire()
                conn_manager = self.connection_manager
                conn_dict = conn_manager.get_dict()

                control_index = conn_dict[self.id][0]
                if self.measurement_result == 1:
                    x(self.state, control_index, self.execution_time, None)
                cnot(self.state, control_index, gate.target_index, self.execution_time, None)
                h(self.state, control_index, self.execution_time, None)

                measurement_result = measure(self.state, control_index, self.execution_time, None)
                self.measurement_result = measurement_result

                qubit = QuantumState(1)
                self.state.add_state(qubit)

                self.connection_manager.remove_qubit(self.id, 0)
                self.connection_manager.add_qubit(self.id, 0)

                link = self.link_list[gate.link_id]
                link.send_target_message(self.measurement_result)

                self.lock.release()

            # Apply operations before the sending back to the measurement result to the control processor
            elif gate.name == "BACKWARD_CONTROL":
                pass

            # Apply operations after the receiving the measurement result from the target processor
            elif gate.name == "BACKWARD_TARGET":
                self.lock.acquire()
                if self.measurement_result == 1:
                    z(self.state, gate.index, self.execution_time, None)
                self.lock.release()
