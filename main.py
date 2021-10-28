from logical.circuit import QuantumCircuit

qn = 2
qc = QuantumCircuit(qn)

qc.x(0)
qc.cx(0, 1)
qc.cx(1, 0)

qc.execute()
state = qc.result()
print(state)
