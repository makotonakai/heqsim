from logical.circuit import QuantumCircuit

qn = 3
qc = QuantumCircuit(qn)
qc.x(0)
qc.x(1)

qc.execute()
state_list = qc.result()
print(state_list)