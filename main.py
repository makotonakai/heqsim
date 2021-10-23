from logical.circuit import QuantumCircuit

qn = 3
qc = QuantumCircuit(qn)
qc.h(0)
qc.cx(0,2)

qc.execute()
state = qc.result()
print(state)

