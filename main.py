from disqs.logical.circuit import QuantumCircuit
from disqs.logical.processor import QuantumProcessor
from disqs.logical.network import Network

p1 = QuantumProcessor(qubit_num=1, execution_time=0.1)
p2 = QuantumProcessor(qubit_num=1, execution_time=0.2)
p3 = QuantumProcessor(qubit_num=1, execution_time=0)

network = Network()
network.add_link(p1, p2)
network.add_link(p2, p3)

qn = 3
qc = QuantumCircuit(qn)
qc.h(0)
qc.cnot(0, 2)

qc.execute(network=network)
result = qc.result()
print(result)
