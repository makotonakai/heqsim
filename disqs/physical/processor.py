from disqs.physical.state import QuantumState
from disqs.physical.gate import x, y, z, h, cnot, measure
from disqs.device.connection import Connection
from threading import Thread
import numpy as np
import queue
import time


class QuantumProcessor(Thread):
    def __init__(self, detail):
        Thread.__init__(self)
        self.id = detail["id"]
        self.qubit_num = detail["qubit_num"]
        self.execution_time = detail["execution_time"]

        self.state = None
        self.lock = None
        self.index_list = None
        self.gate_list = None
        self.connection_list = None

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
                cnot(self.state, gate.index, self.execution_time, self.lock)

            elif gate.name == "RemoteCNOT":

                connection = self.connection_list[gate.id]
                try:
                    connection.send_request(gate.id)
                    ack = connection.get_ack()
                except queue.Full:
                    request = connection.get_request()
                    connection.send_ack("ack")

                if gate.role == "control":

                    bell_pair = QuantumState(2)
                    h(bell_pair, 0, 0, self.lock)
                    cnot(bell_pair, 0, 1, 0, self.lock)

                    self.lock.acquire()
                    self.state.add_state(bell_pair)
                    self.lock.release()

                    cnot(self.state, gate.index, self.state.qubit_num - 2, self.execution_time, self.lock)
                    measure_result = measure(self.state, self.state.qubit_num - 2, self.execution_time, self.lock)
                    connection.send_message(measure_result)
                    ack = connection.get_ack()

                    measure_result = connection.get_message()
                    if measure_result == 1:
                        z(self.state, gate.index, self.execution_time, self.lock)

                elif gate.role == "target":

                    measure_result = connection.get_message()
                    connection.send_ack("ack")

                    if measure_result == 1:
                        x(self.state, self.state.qubit_num - 1, self.execution_time, self.lock)

                    cnot(self.state, self.state.qubit_num - 1, gate.target_index, self.execution_time, self.lock)
                    h(self.state, self.state.qubit_num - 1, self.execution_time, self.lock)
                    measure_result = measure(self.state, self.state.qubit_num - 1, self.execution_time, self.lock)
                    connection.send_message(measure_result)
