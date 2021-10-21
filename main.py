from logical.circuit import QuantumCircuit

qn = 2
qc = QuantumCircuit(qn)
qc.h(0)


qc.execute()
state = qc.result()
print(state)
