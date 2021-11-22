from disqs.physical.state import QuantumState
from disqs.physical.gate import x, y, z, h, cnot, measure, measure_
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

    def run(self):

        for gate in self.gate_list:

            if gate.name == "X":
                x(self.state, gate.index, self.execution_time, self.lock)

            elif gate.name == "Y":
                y(self.state, gate.index, self.execution_time, self.lock)

            elif gate.name == "Z":
                z(self.state, gate.index, self.execution_time, self.lock)

            elif gate.name == "H":
                h(self.state, gate.index, self.execution_time, self.lock)

            elif gate.name == "CNOT":
                cnot(self.state, gate.index, gate.target_index, self.execution_time, self.lock)

            elif gate.name == "RemoteCNOT":

                connection = self.link_list[gate.link_id]
                try:
                    connection.send_request(gate.link_id)
                    ack = connection.get_ack()
                except queue.Full:
                    request = connection.get_request()
                    connection.send_ack()

                if gate.role == "control":

                    bell_pair = QuantumState(2)
                    h(bell_pair, 0, 0, self.lock)
                    cnot(bell_pair, 0, 1, 0, self.lock)

                    self.lock.acquire()
                    self.state.add_state(bell_pair)
                    self.lock.release()

                    cnot(self.state, gate.index, self.state.qubit_num - 2, self.execution_time, self.lock)

                    first_bit = measure(self.state, self.state.qubit_num - 2, self.lock)
                    connection.send_control_message(first_bit)

                    second_bit = connection.get_target_message()
                    if second_bit == 1:
                        z(self.state, gate.target_index, self.execution_time, self.lock)

                elif gate.role == "target":

                    first_bit = connection.get_control_message()
                    if first_bit == 1:
                        x(self.state, self.state.qubit_num - 1, self.execution_time, self.lock)

                    cnot(self.state, self.state.qubit_num - 1, gate.target_index, self.execution_time, self.lock)
                    h(self.state, self.state.qubit_num - 1, self.execution_time, self.lock)

                    second_bit = measure(self.state, self.state.qubit_num - 1, self.lock)
                    connection.send_target_message(second_bit)
