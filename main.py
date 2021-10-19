from logical.circuit import QuantumCircuit
from physical.processor import QuantumProcessor
import ray

qn = 4
qc = QuantumCircuit(qn)
for idx in range(qn):
    qc.x(idx)

qc.execute()
state_list = qc.result()
print(state_list)