from disqs.logical.circuit import QuantumCircuit
from disqs.logical.processor import QuantumProcessor
from disqs.logical.network import Network

p1 = QuantumProcessor(qubit_num=1, execution_time=0.1)
p2 = QuantumProcessor(qubit_num=2, execution_time=0.2)

network = Network()
network.add_link(p1, p2)

qn = 3
qc = QuantumCircuit(qn)

qc.x(0)
qc.cnot(0, 1)

qc.execute(network=network)
# result = qc.result()
# print(result)
