from disqs.logical.circuit import QuantumCircuit
from disqs.logical.processor import QuantumProcessor
from disqs.logical.network import Network
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
p2 = QuantumProcessor(qubit_num=1, execution_time=0.5)

network = Network()
network.add_link(p1, p2)

qn = 2
qc = QuantumCircuit(qn)
# qft(qc)
qc.cnot(0, 1)
qc.execute(network=network)

execution_time = qc.get_execution_time()
print("Time:", execution_time)
