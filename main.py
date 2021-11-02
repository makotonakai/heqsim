from logical.circuit import QuantumCircuit

qn = 3
qc = QuantumCircuit(qn)

qc.x(0)
qc.cx(0, 2)

qc.execute()
result = qc.result()
print(result)
