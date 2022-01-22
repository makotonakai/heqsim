from heqsim.software.circuit import QuantumCircuit
from heqsim.software.processor import QuantumProcessor
from heqsim.software.network import Network
import numpy as np


def qft_helper(qc, qubit_num, start, end):
    if qubit_num == 1:
        qc.h(end)
    else:
        qc.h(start)
        for control in range(start + 1, end + 1):
            qc.cphase(control, start, 2 * np.pi / (2**(control + 1 - start)))
        qft_helper(qc, qubit_num - 1, start + 1, end)


def qft(qc):
    qft_helper(qc, qc.qubit_num, 0, qc.qubit_num - 1)


p1 = QuantumProcessor(qubit_num=1, execution_time=0.1)
p2 = QuantumProcessor(qubit_num=1, execution_time=0.2)
# p3 = QuantumProcessor(qubit_num=1, execution_time=0.3)

network = Network()
network.add_link(p1, p2)
# network.add_link(p2, p3)

qn = 2
qc = QuantumCircuit(qn)
qc.h(0)
qc.cnot(0, 1)
qc.execute(network=network)

result = qc.get_result()
for index in range(len(result)):
    if result[index] != 0:
        print("index:{} prob amp:{}".format(index, result[index]))
# print("Result:", result)

# execution_time = qc.get_execution_time()
# print("Time:", execution_time)
