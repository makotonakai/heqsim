from disqs.physical.state import QuantumState
from disqs.physical.gate import x, y, z, h, cnot, measure, rx, ry, rz, phase
from disqs.device.link import Link
from threading import Thread
import numpy as np
import queue
import time


class PhysicalProcessor(Thread):

    def __init__(self, param):
        Thread.__init__(self)
        self.id = param["id"]
        self.qubit_num = param["qubit_num"]
        self.execution_time = param["execution_time"]

        self.state = None
        self.gate_list = None
        self.link_list = None
        self.lock = None
        self.bell_pair_manager = None

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

            elif gate.name == "RX":
                rx(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            elif gate.name == "RY":
                ry(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            elif gate.name == "RZ":
                rz(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            elif gate.name == "PHASE":
                phase(self.state, gate.index, gate.theta, self.execution_time, self.lock)

            # Remote CNOT gate
            elif gate.name == "RemoteCNOT":

                # Choose a link to use for communication
                connection = self.link_list[gate.link_id]

                # Synchronize the sender and receiver
                try:
                    connection.send_request(gate.link_id)
                    ack = connection.get_ack()
                except queue.Full:
                    request = connection.get_request()
                    connection.send_ack()

                # The sender side
                if gate.role == "control":

                    self.lock.acquire()

                    # Declare the detail of a remote cnot
                    remote_cnot_info = {}
                    qubit_num = self.state.get_qubit_num()
                    remote_cnot_info["qubit_indices"] = [qubit_num, qubit_num + 1]
                    remote_cnot_info["id"] = gate.remote_cnot_id

                    # Submit the info of a remote cnot to the Bell pair manager
                    self.remote_cnot_manager.add_new_info(remote_cnot_info)

                    # Add bell pair
                    bell_pair = QuantumState(2)
                    h(bell_pair, 0, 0, None)
                    cnot(bell_pair, 0, 1, 0, None)
                    self.state.add_state(bell_pair)

                    self.lock.release()

                    # Apply CNOT between the sender and the given bell pair
                    cnot(self.state, gate.index, qubit_num, self.execution_time, self.lock)

                    # Get which qubit to measure
                    control_index = self.remote_cnot_manager.get_control_index(gate.remote_cnot_id)

                    # Perform the first measurement
                    first_bit = measure(self.state, control_index, self.lock)

                    # Send the measurement result over the communication link
                    connection.send_control_message(first_bit)

                    # Get the measurement result of the 2nd measurement
                    second_bit = connection.get_target_message()

                    # If the 2nd measurement result is 1
                    if second_bit == 1:

                        # Apply a Z gate to the control qubit
                        z(self.state, gate.index, self.execution_time, self.lock)

                # The receiver side
                elif gate.role == "target":

                    # Get the measurement result of the 1st measurement
                    first_bit = connection.get_control_message()

                    # If the 1st measurement result is 1
                    if first_bit == 1:

                        # Apply X to the 2nd qubit on the Bell pair
                        x(self.state, self.state.qubit_num - 1, self.execution_time, self.lock)

                    # Apply a CNOT gate between the 2nd qubit on the Bell pair and the target qubit
                    cnot(self.state, self.state.qubit_num - 1, gate.target_index, self.execution_time, self.lock)

                    # Apply a CNOT gate between the 2nd qubit on the Bell pair
                    h(self.state, self.state.qubit_num - 1, self.execution_time, self.lock)

                    # Get which qubit to measure
                    target_index = self.remote_cnot_manager.get_target_index(gate.remote_cnot_id)

                    # Get the measurement result of the 1st measurement
                    second_bit = measure(self.state, target_index, self.lock)

                    # Send the 1st measurement result over the communication link
                    connection.send_target_message(second_bit)
