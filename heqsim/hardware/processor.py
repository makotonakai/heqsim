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
        self.qubit_num = param["qubit_num"]
        self.execution_time = param["execution_time"]

        self.state = None
        self.gate_list = None
        self.link_list = None
        self.lock = None
        self.qubit_index_manager = None
        self.swap_num = 0
        self.tele_num = 0

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
                if gate.role == "remote":
                    self.lock.acquire()
                    comm_index = self.qubit_index_manager.dict["communication"][self.id][0]
                    cnot(self.state, comm_index, gate.target_index, self.execution_time, None)
                    self.lock.release()
                else:
                    cnot(self.state, gate.index, gate.target_index, self.execution_time, self.lock)

            elif gate.name == "RX":
                rx(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            elif gate.name == "RY":
                ry(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            elif gate.name == "RZ":
                rz(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            elif gate.name == "PHASE":
                phase(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            elif gate.name == "SWAP":

                if gate.role == "first":
                    self.lock.acquire()
                    comm_qubit_idx = self.qubit_index_manager.dict["communication"][self.id][0]
                    swap(self.state, gate.index, comm_qubit_idx, self.execution_time, None)
                    self.lock.release()

                elif gate.role == "intermit":
                    self.lock.acquire()
                    comm_qubit_idx = self.qubit_index_manager.dict["communication"][self.id][0]
                    link_qubit_idx = self.qubit_index_manager.dict["link"][gate.link_id][0]
                    swap(self.state, comm_qubit_idx, link_qubit_idx, self.execution_time, None)
                    self.lock.release()

                elif gate.role == "last":
                    self.lock.acquire()
                    comm_qubit_idx = self.qubit_index_manager.dict["link"][gate.link_id][0]
                    swap(self.state, gate.index, comm_qubit_idx, self.execution_time, None)
                    self.lock.release()

                else:
                    swap(self.state, gate.index, gate.target_index, self.execution_time, self.lock)

            # Remote CNOT gate
            elif gate.name == "RemoteCNOT":

                # Choose a link to use for communication
                connection = self.link_list[gate.link_id]

                try:
                    connection.send_request(gate.link_id)
                    ack = connection.get_ack()
                except queue.Full:
                    request = connection.get_request()
                    connection.send_ack()

                if "control" in gate.role:

                    # quantum teleportation

                    self.lock.acquire()
                    first_idx = self.qubit_index_manager.dict["communication"][self.id][0]
                    if "forth" in gate.role:
                        second_idx = self.qubit_index_manager.dict["link"][gate.link_id][0]
                    elif "back" in gate.role:
                        second_idx = self.qubit_index_manager.dict["link"][gate.link_id][1]

                    if "forth" in gate.role:
                        target_idx = self.qubit_index_manager.dict["link"][gate.link_id][1]
                    elif "back" in gate.role:
                        target_idx = self.qubit_index_manager.dict["link"][gate.link_id][0]

                    h(self.state, second_idx, self.execution_time, None)
                    cnot(self.state, second_idx, target_idx, self.execution_time, None)

                    cnot(self.state, first_idx, second_idx, self.execution_time, None)
                    h(self.state, first_idx, self.execution_time, None)

                    first_bit = measure(self.state, first_idx, None)
                    self.qubit_index_manager.delete_index("communication", self.id, 0)

                    second_idx = self.qubit_index_manager.dict["link"][gate.link_id][0]
                    second_bit = measure(self.state, second_idx, None)
                    self.qubit_index_manager.delete_index("link", gate.link_id, 0)

                    connection.send_control_message(first_bit)
                    connection.send_control_message(second_bit)

                    self.lock.release()

                    target = connection.get_target_message()
                    new_qubit = QuantumState(1)
                    self.state.add_state(new_qubit)
                    self.qubit_index_manager.add_index("communication", self.id)

                    connection.send_control_message("hoge")

                elif "target" in gate.role:

                    first_bit = connection.get_control_message()
                    second_bit = connection.get_control_message()
                    target_idx = self.qubit_index_manager.dict["link"][gate.link_id][0]

                    if second_bit == 1:
                        x(self.state, target_idx, self.execution_time, self.lock)

                    if first_bit == 1:
                        z(self.state, target_idx, self.execution_time, self.lock)

                    new_qubit = QuantumState(1)
                    self.state.add_state(new_qubit)
                    self.qubit_index_manager.add_index("link", gate.link_id)

                    connection.send_target_message("target")
                    control = connection.get_control_message()
