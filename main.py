from Logical.Circuit import QuantumCircuit

qc = QuantumCircuit(2)
qc.cx(0,1)
state = qc.get_new_state()
print(state)

