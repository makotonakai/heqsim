from disqs.logical.circuit import QuantumCircuit

qn = 2
qc = QuantumCircuit(qn)

qc.h(0)
qc.cnot(0, 1)

qc.execute()
result = qc.result()
print(result)
