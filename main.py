from logical.circuit import QuantumCircuit

qn = 2
qc = QuantumCircuit(qn)

for idx in range(qn):
    qc.x(idx)
    qc.h(idx)
qc.execute()
# result = qc.result()
# print(result)
