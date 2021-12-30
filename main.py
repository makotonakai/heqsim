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


p1 = QuantumProcessor(qubit_num=4, execution_time=0.1)
p2 = QuantumProcessor(qubit_num=4, execution_time=0.5)

network = Network()
network.add_link(p1, p2)

qn = 6
qc = QuantumCircuit(qn)
qc.h(0)
qc.h(1)
qc.h(2)
qc.cnot(2, 4)
qc.x(3)
qc.cnot(2, 3)
qc.ccnot(0, 1, 3)
qc.x(0)
qc.x(0)
qc.ccnot(0, 1, 3)
qc.x(0)
qc.x(1)
qc.x(3)
qc.h(0)
qc.h(1)
qc.h(2)

qc.execute(network=network, is_optimized=True)

# result = qc.get_result()
# print("Result:", result)

execution_time = qc.get_execution_time()
print("Time:", execution_time)
